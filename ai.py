"""Thin wrapper around the Anthropic API. Every request and full response is saved so the run is auditable."""
import json
import os
import re
from pathlib import Path

import config

_client = None
LOG_DIR = None
_counter = 0


class AIError(RuntimeError):
    pass


def setup(log_dir, client=None):
    """client is only injected by tests. A real run always builds the Anthropic client from ANTHROPIC_API_KEY."""
    global _client, LOG_DIR, _counter
    LOG_DIR, _counter = Path(log_dir), 0
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if client is not None:
        _client = client
        return
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise AIError("ANTHROPIC_API_KEY is not set. Add it to .env. The pipeline will not run without a real model.")
    import anthropic
    _client = anthropic.Anthropic()


def call_tool(name, system, prompt, schema, max_tokens=16000):
    """Asks Claude to answer through one tool so the output is structured JSON. Raises on any failure."""
    global _counter
    tools = [{"name": name, "description": f"Return the {name} result.", "input_schema": schema}]
    messages = [{"role": "user", "content": prompt}]
    system = system + f" Always give your answer by calling the {name} tool, never as plain text."
    for attempt in range(2):
        _counter += 1
        request = {"model": config.MODEL, "max_tokens": max_tokens, "system": system,
                   "messages": messages, "tools": tools, "tool_choice": {"type": "auto"}}
        stem = LOG_DIR / f"{_counter:02d}_{name}"
        stem.with_suffix(".request.json").write_text(json.dumps(request, indent=2, ensure_ascii=False))
        try:
            response = _client.messages.create(**request)
        except Exception as e:  # API errors are reported, never replaced with made-up output
            raise AIError(f"{name}: API call failed: {e}")
        raw = response.model_dump() if hasattr(response, "model_dump") else response
        stem.with_suffix(".response.json").write_text(json.dumps(raw, indent=2, ensure_ascii=False, default=str))
        for block in raw["content"]:
            if block.get("type") == "tool_use" and block.get("name") == name:
                return block["input"]
        messages = [{"role": "user", "content": prompt + f"\n\nReply only by calling the {name} tool."}]
    raise AIError(f"{name}: model did not return a tool result (stop_reason={raw.get('stop_reason')})")


NUM = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)(?:\s?([kKmM])(?![a-zA-Z]))?")


def numbers_in(text):
    """All numbers in a piece of text as floats. 3.3K -> 3300, 1,100 -> 1100."""
    out = []
    for digits, suffix in NUM.findall(text or ""):
        value = float(digits.replace(",", ""))
        if suffix:
            value *= 1000 if suffix.lower() == "k" else 1_000_000
        out.append(value)
    return out


def unsupported_numbers(text, allowed):
    """Numbers in text that don't match an allowed value (to within rounding)."""
    bad = []
    for n in numbers_in(text):
        if not any(abs(n - a) <= max(0.51, abs(a) * 0.02) for a in allowed):
            bad.append(n)
    return bad
