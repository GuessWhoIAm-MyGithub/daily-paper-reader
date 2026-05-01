import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


def _load_module():
    root = Path(__file__).resolve().parents[1]
    src_dir = root / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    src_path = root / "src" / "main.py"
    spec = importlib.util.spec_from_file_location("main_pipeline_mod", src_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class MainPipelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def _write_rrf_input(self, root: Path, token: str) -> Path:
        filtered_dir = root / "archive" / token / "filtered"
        filtered_dir.mkdir(parents=True, exist_ok=True)
        path = filtered_dir / f"arxiv_papers_{token}.json"
        payload = {
            "generated_at": "2026-03-10T00:00:00+00:00",
            "papers": [
                {"id": "p1", "title": "Paper 1", "abstract": "A"},
                {"id": "p2", "title": "Paper 2", "abstract": "B"},
                {"id": "p3", "title": "Paper 3", "abstract": "C"},
            ],
            "queries": [
                {
                    "type": "intent_query",
                    "tag": "query:test",
                    "paper_tag": "query:test",
                    "query_text": "test query",
                    "sim_scores": {
                        "p1": {"score": 0.9, "rank": 1},
                        "p2": {"score": 0.6, "rank": 2},
                        "p3": {"score": 0.2, "rank": 3},
                    },
                }
            ],
        }
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def test_resolve_summary_step_env_keeps_unified_llm_env(self):
        with patch.dict(
            os.environ,
            {
                "LLM_REQUEST_FORMAT": "openai",
                "LLM_BASE_URL": "https://api.openai.com/v1",
                "LLM_API_KEY": "shared-key",
                "LLM_SUMMARY_MODEL": "gpt-4.1-mini",
            },
            clear=True,
        ):
            env = self.mod.resolve_summary_step_env()

        self.assertEqual(env["LLM_REQUEST_FORMAT"], "openai")
        self.assertEqual(env["LLM_BASE_URL"], "https://api.openai.com/v1")
        self.assertEqual(env["LLM_API_KEY"], "shared-key")
        self.assertEqual(env["LLM_SUMMARY_MODEL"], "gpt-4.1-mini")

    def test_prepare_rerank_fallback_builds_ranked_from_sim_scores(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            token = "20260310"
            input_path = self._write_rrf_input(root, token)
            rerank_path = root / "archive" / token / "rank" / f"arxiv_papers_{token}.json"
            ok = self.mod.prepare_rerank_fallback(str(input_path), str(rerank_path))
            self.assertTrue(ok)
            data = json.loads(rerank_path.read_text(encoding="utf-8"))
            ranked = data["queries"][0]["ranked"]
            self.assertEqual([item["paper_id"] for item in ranked], ["p1", "p2", "p3"])
            self.assertEqual(ranked[0]["star_rating"], 5)
            self.assertGreaterEqual(ranked[1]["star_rating"], ranked[2]["star_rating"])

    def test_main_always_runs_rerank_step(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            src_dir = root / "src"
            src_dir.mkdir(parents=True, exist_ok=True)
            token = "20260310"
            self._write_rrf_input(root, token)
            calls = []

            def fake_run_step(label, args, env=None):
                calls.append((label, args, env))

            with patch.object(self.mod, "ROOT_DIR", str(root)), patch.object(
                self.mod, "SRC_DIR", str(src_dir)
            ), patch.object(
                self.mod, "resolve_run_date_token", return_value=token
            ), patch.object(
                self.mod, "resolve_sidebar_date_label", return_value=None
            ), patch.object(
                self.mod, "parse_trace_ids", return_value=[]
            ), patch.object(
                self.mod, "run_step", side_effect=fake_run_step
            ), patch.object(
                sys, "argv", ["main.py"]
            ), patch.dict(
                os.environ,
                {"LLM_BASE_URL": "https://api.openai.com/v1"},
                clear=True,
            ):
                self.mod.main()

            labels = [item[0] for item in calls]
            self.assertIn("Step 3 - Rerank", labels)


if __name__ == "__main__":
    unittest.main()
