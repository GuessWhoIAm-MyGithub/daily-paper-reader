import json
import os
import re
import time
from typing import Any, Dict, List, Optional

import requests


GLOBAL_TOKENS = {
    "prompt": 0,
    "thinking": 0,
    "content": 0,
    "total": 0,
}
GLOBAL_TIME_SECONDS: float = 0.0

DEFAULT_REQUEST_FORMAT = "openai"
DEFAULT_ANTHROPIC_VERSION = "2023-06-01"


def reset_global_tokens():
    GLOBAL_TOKENS["prompt"] = 0
    GLOBAL_TOKENS["thinking"] = 0
    GLOBAL_TOKENS["content"] = 0
    GLOBAL_TOKENS["total"] = 0


def get_global_tokens() -> Dict[str, int]:
    return dict(GLOBAL_TOKENS)


def reset_global_time():
    global GLOBAL_TIME_SECONDS
    GLOBAL_TIME_SECONDS = 0.0


def get_global_time() -> float:
    return float(GLOBAL_TIME_SECONDS)


def normalize_request_format(value: str | None) -> str:
    lowered = str(value or "").strip().lower()
    if lowered in {"anthropic", "claude"}:
        return "anthropic"
    return "openai"


def normalize_base_url(value: str | None) -> str:
    raw = str(value or "").strip().rstrip("/")
    if not raw:
        return ""
    raw = re.sub(r"/chat/completions$", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"/messages$", "", raw, flags=re.IGNORECASE)
    return raw.rstrip("/")


def build_request_url(base_url: str, request_format: str) -> str:
    raw = normalize_base_url(base_url)
    if not raw:
        raise ValueError("缺少可用的 LLM base_url")
    if normalize_request_format(request_format) == "anthropic":
        if raw.lower().endswith("/messages"):
            return raw
        if re.search(r"/v\d+$", raw, re.IGNORECASE):
            return f"{raw}/messages"
        return f"{raw}/v1/messages"
    if raw.lower().endswith("/chat/completions"):
        return raw
    if re.search(r"/v\d+$", raw, re.IGNORECASE):
        return f"{raw}/chat/completions"
    return f"{raw}/v1/chat/completions"


class BaseLLMClient:
    def __init__(self, api_key: str, model: str, base_url: str, request_format: str):
        self.api_key = str(api_key or "").strip()
        self.model = str(model or "").strip()
        self.base_url = normalize_base_url(base_url)
        self.request_format = normalize_request_format(request_format)
        self.tokens = {
            "prompt": 0,
            "content": 0,
            "reasoning": 0,
            "total": 0,
        }
        self._call_index = 0
        self._cum_tokens = {
            "prompt": 0,
            "thinking": 0,
            "content": 0,
            "total": 0,
        }
        self._cum_time_seconds = 0.0
        self.kwargs: Dict[str, Any] = {
            "max_tokens": 4000,
            "temperature": 0.6,
            "top_p": 0.3,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "stream": False,
        }

    @staticmethod
    def _extract_text_content(value: Any) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            parts: List[str] = []
            for item in value:
                text = BaseLLMClient._extract_text_content(item)
                if text:
                    parts.append(text)
            return "\n".join(parts).strip()
        if isinstance(value, dict):
            if value.get("type") == "text":
                return str(value.get("text") or "").strip()
            for key in ("text", "content", "value"):
                text = value.get(key)
                if isinstance(text, str) and text.strip():
                    return text
        return ""

    @staticmethod
    def _strip_json_wrappers(text: str) -> str:
        cleaned = (text or "").strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return cleaned.strip()

    @staticmethod
    def _repair_json_suffix(text: str) -> str:
        if not text:
            return text
        stack: List[str] = []
        in_str = False
        escaped = False
        for ch in text:
            if in_str:
                if escaped:
                    escaped = False
                    continue
                if ch == "\\":
                    escaped = True
                    continue
                if ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch == "{":
                stack.append("}")
            elif ch == "[":
                stack.append("]")
            elif ch in ("}", "]") and stack and stack[-1] == ch:
                stack.pop()
        repaired = text
        if in_str:
            repaired += '"'
        if stack:
            repaired += "".join(reversed(stack))
        repaired = re.sub(r",(\s*[}\]])", r"\1", repaired)
        return repaired

    @classmethod
    def parse_json_content(cls, text: str) -> Any:
        raw = cls._strip_json_wrappers((text or "").strip())
        if not raw:
            return None
        decoder = json.JSONDecoder()
        candidates: List[str] = []
        first_obj = raw.find("{")
        last_obj = raw.rfind("}")
        first_arr = raw.find("[")
        last_arr = raw.rfind("]")
        if first_obj != -1:
            candidates.append(raw[first_obj:])
            if last_obj != -1 and last_obj >= first_obj:
                candidates.append(raw[first_obj:last_obj + 1])
        if first_arr != -1:
            candidates.append(raw[first_arr:])
            if last_arr != -1 and last_arr >= first_arr:
                candidates.append(raw[first_arr:last_arr + 1])
        candidates.append(raw)

        seen: set[str] = set()
        last_exc: Exception | None = None
        for candidate in candidates:
            if candidate in seen:
                continue
            seen.add(candidate)
            try:
                obj, _idx = decoder.raw_decode(candidate)
                return obj
            except Exception as exc:
                last_exc = exc
                repaired = cls._repair_json_suffix(candidate)
                if repaired == candidate:
                    continue
                try:
                    return json.loads(repaired)
                except Exception as exc2:
                    last_exc = exc2
        raise ValueError(f"模型未返回合法 JSON：{raw[:500]}") from last_exc

    @staticmethod
    def build_json_schema_response_format(
        schema_name: str,
        schema: Dict[str, Any],
        strict: bool = True,
    ) -> Dict[str, Any]:
        return {
            "type": "json_schema",
            "json_schema": {
                "name": schema_name,
                "schema": schema,
                "strict": bool(strict),
            },
        }

    @staticmethod
    def build_json_object_response_format() -> Dict[str, str]:
        return {"type": "json_object"}

    @staticmethod
    def _is_structured_output_unsupported_error(error: Exception) -> bool:
        response = getattr(error, "response", None)
        status_code = getattr(response, "status_code", None)
        text = ""
        if response is not None:
            try:
                text = response.text or ""
            except Exception:
                text = ""
        if not text:
            text = str(error or "")
        lowered = text.lower()
        has_target = any(
            token in lowered
            for token in (
                "response_format",
                "json_schema",
                "json object",
                "json_object",
            )
        )
        has_signal = any(
            token in lowered
            for token in (
                "unsupported",
                "not support",
                "not supported",
                "invalid",
                "unknown",
                "unrecognized",
                "extra inputs",
                "unexpected",
                "must be one of",
                "one of",
                "allowed values",
                "enum",
            )
        )
        if has_target and has_signal:
            return True
        if status_code in (400, 404, 415, 422) and "response_format" in lowered:
            return True
        return False

    def _record_usage(
        self,
        *,
        prompt_tokens: int = 0,
        content_tokens: int = 0,
        reasoning_tokens: int = 0,
        total_tokens: int = 0,
        started_at: float,
    ) -> None:
        self.tokens["prompt"] += int(prompt_tokens)
        self.tokens["content"] += int(content_tokens)
        self.tokens["reasoning"] += int(reasoning_tokens)
        self.tokens["total"] += int(total_tokens)

        GLOBAL_TOKENS["prompt"] += int(prompt_tokens)
        GLOBAL_TOKENS["thinking"] += int(reasoning_tokens)
        GLOBAL_TOKENS["content"] += int(content_tokens)
        GLOBAL_TOKENS["total"] += int(total_tokens)

        elapsed = time.time() - started_at
        self._cum_time_seconds += float(elapsed)
        global GLOBAL_TIME_SECONDS
        GLOBAL_TIME_SECONDS += float(elapsed)

        self._call_index += 1
        self._cum_tokens["prompt"] += int(prompt_tokens)
        self._cum_tokens["thinking"] += int(reasoning_tokens)
        self._cum_tokens["content"] += int(content_tokens)
        self._cum_tokens["total"] += int(total_tokens)

        header = f"[{self.request_format}][{self.model}] 第{self._call_index}次"
        line_cur = (
            f"本次 tokens：prompt={int(prompt_tokens)}, thinking={int(reasoning_tokens)}, "
            f"content={int(content_tokens)}, total={int(total_tokens)}"
        )
        line_cum = (
            f"累计 tokens：prompt={self._cum_tokens['prompt']}, thinking={self._cum_tokens['thinking']}, "
            f"content={self._cum_tokens['content']}, total={self._cum_tokens['total']}"
        )
        line_time = f"本次用时：{elapsed:.2f}s，累计用时：{self._cum_time_seconds:.2f}s"
        print(header + "\n" + line_cur + "\n" + line_cum + "\n" + line_time)

    def chat(
        self,
        messages: List[Dict[str, Any]],
        response_format: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError

    def chat_structured(
        self,
        messages: List[Dict[str, Any]],
        schema_name: str,
        schema: Dict[str, Any],
        *,
        strict: bool = True,
        allow_json_object_fallback: bool = True,
    ) -> Dict[str, Any]:
        attempts: List[tuple[str, Dict[str, Any] | None]] = [
            (
                "json_schema",
                self.build_json_schema_response_format(
                    schema_name=schema_name,
                    schema=schema,
                    strict=strict,
                ),
            )
        ]
        if allow_json_object_fallback:
            attempts.append(("json_object", self.build_json_object_response_format()))

        last_error: Exception | None = None
        for idx, (format_name, response_format) in enumerate(attempts):
            try:
                response = self.chat(messages=messages, response_format=response_format)
            except Exception as exc:
                last_error = exc
                if idx + 1 < len(attempts) and self._is_structured_output_unsupported_error(exc):
                    print(f"[INFO] Structured Outputs 不受支持，回退到 {attempts[idx + 1][0]}。")
                    continue
                raise

            parsed = None
            parse_error: Exception | None = None
            if not response.get("refusal"):
                content = str(response.get("content") or "").strip()
                if content:
                    try:
                        parsed = self.parse_json_content(content)
                    except Exception as exc:
                        parse_error = exc

            structured = dict(response)
            structured["parsed"] = parsed
            structured["parse_error"] = parse_error
            structured["response_format_used"] = format_name
            return structured

        if last_error is not None:
            raise last_error
        raise RuntimeError("结构化输出请求未命中可用格式")


class OpenAICompatibleClient(BaseLLMClient):
    def __init__(self, api_key: str, model: str, base_url: str):
        super().__init__(
            api_key=api_key,
            model=model,
            base_url=base_url,
            request_format="openai",
        )

    def chat(
        self,
        messages: List[Dict[str, Any]],
        response_format: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }
        allowed_keys = {
            "max_tokens",
            "temperature",
            "top_p",
            "n",
            "stream",
            "presence_penalty",
            "frequency_penalty",
            "stop",
            "logprobs",
            "tools",
            "tool_choice",
            "logit_bias",
        }
        if isinstance(self.kwargs, dict):
            for key, value in self.kwargs.items():
                if key in allowed_keys:
                    payload[key] = value
        if response_format is not None:
            payload["response_format"] = response_format
        if isinstance(payload.get("max_tokens"), int) and payload["max_tokens"] > 10000:
            payload["max_tokens"] = 10000

        started_at = time.time()
        request_url = build_request_url(self.base_url, self.request_format)
        response = requests.post(request_url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        response_data = response.json()
        if os.getenv("LLM_DEBUG_RAW") == "1":
            print("[DEBUG] 原始响应包:", response.text)
        if isinstance(response_data, dict) and "error" in response_data:
            raise requests.exceptions.HTTPError(f"API error: {response_data['error']}")
        if "choices" not in response_data or not response_data["choices"]:
            raise requests.exceptions.HTTPError("API response missing choices")

        choice = response_data["choices"][0] if isinstance(response_data["choices"][0], dict) else {}
        message = choice.get("message", {}) if isinstance(choice, dict) else {}
        content = self._extract_text_content(message.get("content"))
        reasoning_content = self._extract_text_content(
            message.get("reasoning_content") or message.get("thinking")
        )
        refusal = str(message.get("refusal") or "").strip()
        finish_reason = choice.get("finish_reason") if isinstance(choice, dict) else None

        usage = response_data.get("usage", {}) or {}
        prompt_tokens = int(usage.get("prompt_tokens", 0) or 0)
        completion_tokens = int(usage.get("completion_tokens", 0) or 0)
        total_tokens = int(usage.get("total_tokens", 0) or 0)
        reasoning_tokens = int(
            (((usage.get("completion_tokens_details") or {}) or {}).get("reasoning_tokens", 0) or 0)
        )
        self._record_usage(
            prompt_tokens=prompt_tokens,
            content_tokens=max(completion_tokens - reasoning_tokens, 0),
            reasoning_tokens=reasoning_tokens,
            total_tokens=total_tokens,
            started_at=started_at,
        )

        return {
            "content": content,
            "raw_content": message.get("content"),
            "reasoning_content": reasoning_content,
            "refusal": refusal,
            "finish_reason": finish_reason,
            "message": message,
            "raw_response": response_data,
            "tokens": {
                "prompt": prompt_tokens,
                "content": max(completion_tokens - reasoning_tokens, 0),
                "reasoning": reasoning_tokens,
                "total": total_tokens,
            },
        }


class AnthropicClient(BaseLLMClient):
    def __init__(self, api_key: str, model: str, base_url: str):
        super().__init__(
            api_key=api_key,
            model=model,
            base_url=base_url,
            request_format="anthropic",
        )

    @staticmethod
    def _convert_messages(messages: List[Dict[str, Any]]) -> tuple[str, List[Dict[str, str]]]:
        system_parts: List[str] = []
        output: List[Dict[str, str]] = []
        for message in messages or []:
            if not isinstance(message, dict):
                continue
            role = str(message.get("role") or "").strip().lower()
            content = BaseLLMClient._extract_text_content(message.get("content"))
            if not content:
                continue
            if role == "system":
                system_parts.append(content)
                continue
            target_role = "assistant" if role == "assistant" else "user"
            if output and output[-1]["role"] == target_role:
                output[-1]["content"] += "\n\n" + content
            else:
                output.append({"role": target_role, "content": content})
        return "\n\n".join(system_parts).strip(), output

    @staticmethod
    def _build_schema_hint(response_format: Dict[str, Any] | None) -> str:
        if not isinstance(response_format, dict):
            return ""
        if response_format.get("type") == "json_schema":
            schema_node = response_format.get("json_schema") or {}
            schema = schema_node.get("schema") or {}
            parts = ["Return only valid JSON."]
            if schema_node.get("name"):
                parts.append(f"Schema name: {schema_node['name']}.")
            if schema:
                parts.append(f"JSON schema: {json.dumps(schema, ensure_ascii=False)}.")
            return " ".join(parts)
        if response_format.get("type") == "json_object":
            return "Return only a valid JSON object with no markdown fences or extra text."
        return ""

    def chat(
        self,
        messages: List[Dict[str, Any]],
        response_format: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": DEFAULT_ANTHROPIC_VERSION,
        }
        system_text, converted_messages = self._convert_messages(messages)
        schema_hint = self._build_schema_hint(response_format)
        merged_system = "\n\n".join(part for part in (system_text, schema_hint) if part).strip()
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": converted_messages,
            "max_tokens": int(self.kwargs.get("max_tokens", 4000) or 4000),
            "stream": False,
        }
        if merged_system:
            payload["system"] = merged_system
        if "temperature" in self.kwargs:
            payload["temperature"] = float(self.kwargs["temperature"])

        started_at = time.time()
        request_url = build_request_url(self.base_url, self.request_format)
        response = requests.post(request_url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        response_data = response.json()
        if os.getenv("LLM_DEBUG_RAW") == "1":
            print("[DEBUG] 原始响应包:", response.text)

        content = self._extract_text_content(response_data.get("content"))
        refusal = ""
        stop_reason = str(response_data.get("stop_reason") or "").strip()
        if stop_reason == "refusal":
            refusal = content
        usage = response_data.get("usage", {}) or {}
        prompt_tokens = int(usage.get("input_tokens", 0) or 0)
        output_tokens = int(usage.get("output_tokens", 0) or 0)
        total_tokens = prompt_tokens + output_tokens
        self._record_usage(
            prompt_tokens=prompt_tokens,
            content_tokens=output_tokens,
            reasoning_tokens=0,
            total_tokens=total_tokens,
            started_at=started_at,
        )

        return {
            "content": content,
            "raw_content": response_data.get("content"),
            "reasoning_content": "",
            "refusal": refusal,
            "finish_reason": stop_reason or None,
            "message": response_data,
            "raw_response": response_data,
            "tokens": {
                "prompt": prompt_tokens,
                "content": output_tokens,
                "reasoning": 0,
                "total": total_tokens,
            },
        }


class LLMClient(OpenAICompatibleClient):
    pass


class ClientFactory:
    @staticmethod
    def from_config(config: Dict[str, Any] | None = None):
        safe = config if isinstance(config, dict) else {}
        request_format = normalize_request_format(
            safe.get("request_format") or safe.get("requestFormat")
        )
        base_url = normalize_base_url(safe.get("base_url") or safe.get("baseUrl"))
        api_key = str(safe.get("api_key") or safe.get("apiKey") or "").strip()
        model = str(safe.get("model") or "").strip()
        if not base_url:
            raise ValueError("缺少必要配置: base_url")
        if not api_key:
            raise ValueError("缺少必要配置: api_key")
        if not model:
            raise ValueError("缺少必要配置: model")
        if request_format == "anthropic":
            return AnthropicClient(api_key=api_key, model=model, base_url=base_url)
        return OpenAICompatibleClient(api_key=api_key, model=model, base_url=base_url)

    @staticmethod
    def from_env(model_env_name: str = "LLM_MODEL"):
        return ClientFactory.from_config(
            {
                "request_format": os.getenv("LLM_REQUEST_FORMAT", DEFAULT_REQUEST_FORMAT),
                "base_url": os.getenv("LLM_BASE_URL", ""),
                "api_key": os.getenv("LLM_API_KEY", ""),
                "model": os.getenv(model_env_name, ""),
            }
        )
