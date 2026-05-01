#!/usr/bin/env python
# 使用统一 LLM 配置对候选论文做批量相关性打分。

import argparse
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from llm import ClientFactory

SCRIPT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
TODAY_STR = str(os.getenv("DPR_RUN_DATE") or "").strip() or datetime.now(timezone.utc).strftime("%Y%m%d")
ARCHIVE_DIR = os.path.join(ROOT_DIR, "archive", TODAY_STR)
FILTERED_DIR = os.path.join(ARCHIVE_DIR, "filtered")
RANKED_DIR = os.path.join(ARCHIVE_DIR, "rank")

MAX_CHARS_PER_DOC = 850
BATCH_SIZE = 24
RRF_K = 60
LANE_TOP_K_BASE = 30
LANE_TOP_K_STEP = 10
LANE_TOP_K_MAX = 120
GLOBAL_POOL_GUARANTEED_MIN = 5
GLOBAL_POOL_GUARANTEED_MAX = 20
GLOBAL_POOL_RRF_MIN = 60
GLOBAL_POOL_RRF_MAX = 300
MAX_BATCH_RETRIES = 2


def log(message: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {message}", flush=True)


def group_start(title: str) -> None:
    print(f"::group::{title}", flush=True)


def group_end() -> None:
    print("::endgroup::", flush=True)


def score_to_stars(score: float) -> int:
    if score >= 0.9:
        return 5
    if score >= 0.5:
        return 4
    if score >= 0.1:
        return 3
    if score >= 0.01:
        return 2
    return 1


def load_json(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"找不到文件：{path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Dict[str, Any], path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log(f"[INFO] 已将打分结果写入：{path}")


def format_doc(title: str, abstract: str) -> str:
    content = f"Title: {title}\nAbstract: {abstract}".strip()
    if len(content) > MAX_CHARS_PER_DOC:
        content = content[:MAX_CHARS_PER_DOC]
    return content


def build_documents(
    papers_by_id: Dict[str, Dict[str, Any]],
    paper_ids: List[str],
) -> List[Dict[str, str]]:
    docs: List[Dict[str, str]] = []
    for pid in paper_ids:
        paper = papers_by_id.get(pid) or {}
        title = str(paper.get("title") or "").strip()
        abstract = str(paper.get("abstract") or "").strip()
        docs.append(
            {
                "id": pid,
                "content": format_doc(title, abstract) if title or abstract else f"[Empty paper {pid}]",
            }
        )
    return docs


def get_top_ids(query_obj: Dict[str, Any]) -> List[str]:
    sim_scores = query_obj.get("sim_scores") or {}
    top_ids = query_obj.get("top_ids") or []
    if not top_ids and isinstance(sim_scores, dict) and sim_scores:
        top_ids = sorted(sim_scores.keys(), key=lambda pid: sim_scores[pid].get("rank", 1e9))
    return list(top_ids)


def _unique_keep_order(items: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for item in items:
        pid = str(item or "").strip()
        if not pid or pid in seen:
            continue
        seen.add(pid)
        out.append(pid)
    return out


def _clamp_int(value: float | int, min_value: int, max_value: int) -> int:
    return max(min_value, min(int(value), max_value))


def resolve_global_pool_budget(
    total_papers: int,
    intent_query_count: int,
) -> Tuple[int, int, int]:
    total = max(int(total_papers or 0), 0)
    intent_count = max(int(intent_query_count or 0), 1)
    if total <= 0:
        lane_top_k = LANE_TOP_K_BASE
    else:
        blocks = (total - 1) // 1000
        lane_top_k = min(LANE_TOP_K_BASE + LANE_TOP_K_STEP * blocks, LANE_TOP_K_MAX)
    guaranteed_per_lane = _clamp_int(
        round(lane_top_k * 0.25),
        GLOBAL_POOL_GUARANTEED_MIN,
        GLOBAL_POOL_GUARANTEED_MAX,
    )
    global_rrf_top = _clamp_int(
        lane_top_k * intent_count,
        GLOBAL_POOL_RRF_MIN,
        GLOBAL_POOL_RRF_MAX,
    )
    return lane_top_k, guaranteed_per_lane, global_rrf_top


def build_global_candidate_ids(
    queries: List[Dict[str, Any]],
    *,
    guaranteed_per_lane: int,
    global_limit: int,
) -> List[str]:
    score_map: Dict[str, float] = {}
    hit_count: Dict[str, int] = {}
    guaranteed_ids: List[str] = []

    for q in queries or []:
        top_ids = get_top_ids(q)
        if not top_ids:
            continue
        if guaranteed_per_lane > 0:
            guaranteed_ids.extend(top_ids[:guaranteed_per_lane])
        for rank_idx, pid in enumerate(top_ids, start=1):
            paper_id = str(pid or "").strip()
            if not paper_id:
                continue
            score_map[paper_id] = score_map.get(paper_id, 0.0) + 1.0 / (RRF_K + rank_idx)
            hit_count[paper_id] = hit_count.get(paper_id, 0) + 1

    ranked = sorted(
        score_map.items(),
        key=lambda item: (-item[1], -hit_count.get(item[0], 0), item[0]),
    )
    global_ids = [pid for pid, _score in ranked]
    if global_limit > 0:
        global_ids = global_ids[:global_limit]
    return _unique_keep_order(list(guaranteed_ids) + list(global_ids))


def build_ranked_from_sim_scores(query_obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    sim_scores = query_obj.get("sim_scores")
    if not isinstance(sim_scores, dict) or not sim_scores:
        return []
    items: list[tuple[str, float | None, int | None]] = []
    for pid, meta in sim_scores.items():
        score = None
        rank = None
        if isinstance(meta, dict):
            raw_score = meta.get("score")
            raw_rank = meta.get("rank")
            if isinstance(raw_score, (int, float)):
                score = float(raw_score)
            if isinstance(raw_rank, (int, float)):
                rank = int(raw_rank)
        elif isinstance(meta, (int, float)):
            score = float(meta)
        items.append((str(pid), score, rank))
    items.sort(
        key=lambda item: (
            item[2] is None,
            item[2] if item[2] is not None else 10**9,
            -(item[1] if item[1] is not None else 0.0),
            item[0],
        )
    )
    if not items:
        return []
    numeric_scores = [item[1] for item in items if item[1] is not None]
    min_score = min(numeric_scores) if numeric_scores else None
    max_score = max(numeric_scores) if numeric_scores else None
    total = len(items)
    ranked: list[dict[str, Any]] = []
    for idx, (pid, score, _rank) in enumerate(items, start=1):
        if (
            score is not None
            and min_score is not None
            and max_score is not None
            and max_score > min_score
        ):
            normalized = (score - min_score) / (max_score - min_score)
        elif total == 1:
            normalized = 1.0
        else:
            normalized = (total - idx) / (total - 1)
        ranked.append(
            {
                "paper_id": pid,
                "score": float(normalized),
                "star_rating": score_to_stars(float(normalized)),
            }
        )
    return ranked


def chunk_docs(docs: List[Dict[str, str]], batch_size: int) -> List[List[Dict[str, str]]]:
    if batch_size <= 0:
        batch_size = 1
    return [docs[i : i + batch_size] for i in range(0, len(docs), batch_size)]


def validate_batch_results(
    batch_docs: List[Dict[str, str]],
    results: Any,
) -> List[Dict[str, Any]]:
    expected_ids = [str(doc.get("id") or "").strip() for doc in batch_docs]
    expected_ids = [pid for pid in expected_ids if pid]
    if not isinstance(results, list):
        raise ValueError("results must be a list")

    output: Dict[str, Dict[str, Any]] = {}
    for item in results:
        if not isinstance(item, dict):
            continue
        pid = str(item.get("id") or "").strip()
        if not pid or pid not in expected_ids or pid in output:
            continue
        score = float(item.get("score", 0.0) or 0.0)
        output[pid] = {
            "id": pid,
            "score": max(0.0, min(score, 10.0)),
            "reason": str(item.get("reason") or "").strip(),
        }
    missing = [pid for pid in expected_ids if pid not in output]
    if missing:
        raise ValueError(f"missing ids={','.join(missing)}")
    return [output[pid] for pid in expected_ids]


def score_batch(
    client,
    query_text: str,
    batch_docs: List[Dict[str, str]],
    retry_note: str = "",
) -> List[Dict[str, Any]]:
    schema = {
        "type": "object",
        "properties": {
            "results": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "score": {"type": "number"},
                        "reason": {"type": "string"},
                    },
                    "required": ["id", "score", "reason"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["results"],
        "additionalProperties": False,
    }
    system_prompt = (
        "You are an academic retrieval reranker. "
        "Score each candidate paper for relevance to the query from 0 to 10. "
        "Use semantic relevance, method fit, task fit, and likely usefulness. "
        "Return JSON only."
    )
    user_prompt = (
        f"Query:\n{query_text}\n\n"
        "Candidate papers:\n"
        f"{json.dumps(batch_docs, ensure_ascii=False)}\n\n"
        "Return exactly one result for every candidate paper. "
        "Do not omit ids. Do not add extra ids. "
        "score is a float in [0,10]. "
        "reason must be a short English phrase (<= 18 words)."
    )
    if retry_note:
        user_prompt += f"\n\nRetry note:\n{retry_note}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    client.kwargs.update({"temperature": 0.0, "max_tokens": 3000})
    response = client.chat_structured(
        messages=messages,
        schema_name="rerank_batch_scores",
        schema=schema,
        strict=True,
        allow_json_object_fallback=True,
    )
    if response.get("refusal"):
        raise ValueError(f"structured output refusal: {response.get('refusal')}")
    if response.get("finish_reason") not in (None, "stop", "end_turn"):
        raise ValueError(f"unexpected finish_reason: {response.get('finish_reason')}")
    if response.get("parse_error") is not None:
        raise response["parse_error"]
    payload = response.get("parsed")
    if not isinstance(payload, dict):
        raise ValueError("parsed payload is not an object")
    return validate_batch_results(batch_docs, payload.get("results") or [])


def score_query_candidates(
    client,
    query_text: str,
    docs: List[Dict[str, str]],
) -> List[Dict[str, Any]]:
    merged: Dict[str, Dict[str, Any]] = {}
    batches = chunk_docs(docs, BATCH_SIZE)
    for batch_idx, batch_docs in enumerate(batches, start=1):
        last_error: Exception | None = None
        for attempt in range(1, MAX_BATCH_RETRIES + 1):
            retry_note = ""
            if last_error is not None:
                retry_note = (
                    f"Attempt {attempt}. Previous output invalid: {last_error}. "
                    f"Return exactly these ids once: {', '.join(doc['id'] for doc in batch_docs)}."
                )
            try:
                results = score_batch(client, query_text, batch_docs, retry_note=retry_note)
                for item in results:
                    merged[item["id"]] = item
                break
            except Exception as exc:
                last_error = exc
                log(f"[WARN] batch {batch_idx}/{len(batches)} attempt {attempt} failed: {exc}")
                if attempt >= MAX_BATCH_RETRIES:
                    raise
    return [merged[doc["id"]] for doc in docs if doc["id"] in merged]


def normalize_ranked_scores(
    scored_items: List[Dict[str, Any]],
    top_n: Optional[int],
) -> List[Dict[str, Any]]:
    ordered = sorted(
        scored_items,
        key=lambda item: (-float(item.get("score", 0.0) or 0.0), str(item.get("id") or "")),
    )
    if top_n is not None:
        ordered = ordered[:top_n]
    if not ordered:
        return []
    raw_scores = [float(item.get("score", 0.0) or 0.0) for item in ordered]
    min_score = min(raw_scores)
    max_score = max(raw_scores)
    normalized: List[Dict[str, Any]] = []
    for item in ordered:
        raw_score = float(item.get("score", 0.0) or 0.0)
        if max_score > min_score:
            score = (raw_score - min_score) / (max_score - min_score)
        elif raw_score > 0:
            score = 1.0
        else:
            score = 0.0
        normalized.append(
            {
                "paper_id": item["id"],
                "score": float(score),
                "star_rating": score_to_stars(float(score)),
                "reason": str(item.get("reason") or "").strip(),
                "raw_score": raw_score,
            }
        )
    return normalized


def process_file(
    client,
    input_path: str,
    output_path: str,
    top_n: Optional[int],
) -> None:
    data = load_json(input_path)
    papers_list = data.get("papers") or []
    all_queries = data.get("queries") or []
    if not papers_list or not all_queries:
        log(f"[WARN] 文件 {os.path.basename(input_path)} 中缺少 papers 或 queries，跳过。")
        return

    def _is_intent_rerank_query(q: Dict[str, Any]) -> bool:
        q_type = str(q.get("type") or "").strip().lower()
        return q_type in {"intent_query", "llm_query"}

    queries = [q for q in all_queries if _is_intent_rerank_query(q)]
    if not queries:
        log("[WARN] 当前输入中没有可用于 rerank 的意图查询，跳过 rerank。")
        data["reranked_at"] = datetime.now(timezone.utc).isoformat()
        save_json(data, output_path)
        return

    papers_by_id = {str(p.get("id")): p for p in papers_list if p.get("id")}
    lane_top_k, guaranteed_per_lane, global_rrf_top = resolve_global_pool_budget(
        len(papers_list),
        len(queries),
    )
    global_candidate_ids = build_global_candidate_ids(
        all_queries,
        guaranteed_per_lane=guaranteed_per_lane,
        global_limit=global_rrf_top,
    )
    data["global_candidate_ids"] = global_candidate_ids
    data["global_pool_lane_top_k"] = lane_top_k
    data["global_pool_limit"] = global_rrf_top
    data["global_pool_guaranteed_per_lane"] = guaranteed_per_lane
    if not global_candidate_ids:
        log("[WARN] 未能从任意 query 中构建统一候选池，改用 sim_scores fallback。")
        for q in queries:
            q["ranked"] = build_ranked_from_sim_scores(q)
        data["reranked_at"] = datetime.now(timezone.utc).isoformat()
        save_json(data, output_path)
        return

    group_start(f"Step 3 - rerank {os.path.basename(input_path)}")
    log(
        f"[INFO] 开始 rerank：queries={len(queries)}（仅 intent/语义查询），papers={len(papers_list)}，"
        f"global_pool={len(global_candidate_ids)}（lane_top_k={lane_top_k}, "
        f"guaranteed_per_lane={guaranteed_per_lane}, global_top={global_rrf_top}），"
        f"batch_size={BATCH_SIZE}"
    )

    for q_idx, q in enumerate(queries, start=1):
        q_text = (q.get("rewrite") or q.get("query_text") or "").strip()
        if not q_text:
            q["ranked"] = build_ranked_from_sim_scores(q)
            continue

        group_start(f"Query {q_idx}/{len(queries)} tag={q.get('tag') or ''}")
        docs = build_documents(papers_by_id, list(global_candidate_ids))
        log(
            f"[INFO] Query {q_idx}/{len(queries)} tag={q.get('tag') or ''} | "
            f"candidates={len(docs)} | batches={len(chunk_docs(docs, BATCH_SIZE))}"
        )
        try:
            scored_items = score_query_candidates(client, q_text, docs)
            q["ranked"] = normalize_ranked_scores(scored_items, top_n=top_n)
        except Exception as exc:
            log(f"[WARN] Query {q_idx} rerank 失败，回退到 sim_scores：{exc}")
            q["ranked"] = build_ranked_from_sim_scores(q)
        finally:
            group_end()

    data["reranked_at"] = datetime.now(timezone.utc).isoformat()
    save_json(data, output_path)
    group_end()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="步骤 3：使用统一 LLM 配置对候选论文做通用批量相关性打分。",
    )
    parser.add_argument(
        "--input",
        type=str,
        default=os.path.join(FILTERED_DIR, f"arxiv_papers_{TODAY_STR}.json"),
        help="筛选结果 JSON 路径。",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=os.path.join(RANKED_DIR, f"arxiv_papers_{TODAY_STR}.json"),
        help="打分后的输出 JSON 路径。",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=None,
        help="最终保留的 Top N（默认保留全部候选）。",
    )
    parser.add_argument(
        "--rerank-model",
        type=str,
        default=os.getenv("LLM_RERANK_MODEL") or "gpt-4.1-mini",
        help="rerank 模型名称。",
    )
    args = parser.parse_args()

    input_path = args.input
    if not os.path.isabs(input_path):
        input_path = os.path.abspath(os.path.join(ROOT_DIR, input_path))

    output_path = args.output
    if not os.path.isabs(output_path):
        output_path = os.path.abspath(os.path.join(ROOT_DIR, output_path))

    if not os.path.exists(input_path):
        log(f"[WARN] 输入文件不存在（今天可能没有新论文）：{input_path}，将跳过 Step 3。")
        return

    if not str(os.getenv("LLM_API_KEY") or "").strip():
        raise RuntimeError("缺少 LLM_API_KEY 环境变量，无法调用统一 LLM 评分。")

    client = ClientFactory.from_config(
        {
            "request_format": os.getenv("LLM_REQUEST_FORMAT"),
            "base_url": os.getenv("LLM_BASE_URL"),
            "api_key": os.getenv("LLM_API_KEY"),
            "model": args.rerank_model,
        }
    )
    process_file(
        client=client,
        input_path=input_path,
        output_path=output_path,
        top_n=args.top_n,
    )


if __name__ == "__main__":
    main()
