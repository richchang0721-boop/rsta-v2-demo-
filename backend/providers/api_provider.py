"""
API Provider
============
Supports:
  - OpenAI compatible (OpenAI, OpenRouter, custom endpoint)
  - Anthropic
  - Google Gemini
  - Ollama (local)
  - LM Studio (local OpenAI-compatible)
"""

import httpx
from typing import Optional

PROVIDER_NAME = "api"

PROVIDER_CONFIGS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "chat_path": "/chat/completions",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "default_model": "gpt-4o-mini",
        "style": "openai",
    },
    "anthropic": {
        "base_url": "https://api.anthropic.com",
        "chat_path": "/v1/messages",
        "auth_header": "x-api-key",
        "auth_prefix": "",
        "default_model": "claude-haiku-4-5-20251001",
        "style": "anthropic",
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com",
        "chat_path": "/v1beta/models/{model}:generateContent",
        "auth_header": None,
        "auth_prefix": "",
        "default_model": "gemini-1.5-flash",
        "style": "gemini",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "chat_path": "/chat/completions",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "default_model": "meta-llama/llama-3-8b-instruct:free",
        "style": "openai",
    },
    "ollama": {
        "base_url": "http://localhost:11434",
        "chat_path": "/api/chat",
        "auth_header": None,
        "auth_prefix": "",
        "default_model": "llama3",
        "style": "ollama",
    },
    "lmstudio": {
        "base_url": "http://localhost:1234/v1",
        "chat_path": "/chat/completions",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "default_model": "local-model",
        "style": "openai",
    },
}


async def is_available(provider_id: str, api_key: str = "") -> bool:
    cfg = PROVIDER_CONFIGS.get(provider_id)
    if not cfg:
        return False
    if provider_id in ("ollama", "lmstudio"):
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                r = await client.get(cfg["base_url"])
                return r.status_code < 500
        except Exception:
            return False
    return bool(api_key)


async def generate(
    prompt: str,
    system_prompt: str = "",
    provider_id: str = "openai",
    api_key: str = "",
    model: str = "",
    **kwargs,
) -> str:
    cfg = PROVIDER_CONFIGS.get(provider_id)
    if not cfg:
        raise ValueError(f"Unknown provider: {provider_id}")

    use_model = model or cfg["default_model"]
    style = cfg["style"]

    headers = {"Content-Type": "application/json"}
    if cfg["auth_header"] and api_key:
        headers[cfg["auth_header"]] = cfg["auth_prefix"] + api_key

    if style == "openai":
        return await _openai_call(cfg, headers, system_prompt, prompt, use_model)
    elif style == "anthropic":
        headers["anthropic-version"] = "2023-06-01"
        return await _anthropic_call(cfg, headers, system_prompt, prompt, use_model)
    elif style == "gemini":
        return await _gemini_call(cfg, api_key, system_prompt, prompt, use_model)
    elif style == "ollama":
        return await _ollama_call(cfg, system_prompt, prompt, use_model)
    else:
        raise ValueError(f"Unknown style: {style}")


async def _openai_call(cfg, headers, system_prompt, prompt, model):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    url = cfg["base_url"] + cfg["chat_path"]
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(url, headers=headers,
                              json={"model": model, "messages": messages, "max_tokens": 512})
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]


async def _anthropic_call(cfg, headers, system_prompt, prompt, model):
    body = {
        "model": model,
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system_prompt:
        body["system"] = system_prompt
    url = cfg["base_url"] + cfg["chat_path"]
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(url, headers=headers, json=body)
        r.raise_for_status()
        return r.json()["content"][0]["text"]


async def _gemini_call(cfg, api_key, system_prompt, prompt, model):
    path = cfg["chat_path"].replace("{model}", model)
    url = cfg["base_url"] + path + f"?key={api_key}"
    contents = [{"parts": [{"text": prompt}]}]
    body = {"contents": contents}
    if system_prompt:
        body["systemInstruction"] = {"parts": [{"text": system_prompt}]}
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(url, json=body)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]


async def _ollama_call(cfg, system_prompt, prompt, model):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    url = cfg["base_url"] + cfg["chat_path"]
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(url, json={"model": model, "messages": messages, "stream": False})
        r.raise_for_status()
        return r.json()["message"]["content"]
