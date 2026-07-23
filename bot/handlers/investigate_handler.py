import logging
from collections import Counter

import httpx
from aiogram import Router
from aiogram.types import Message

from bot.config import config

logger = logging.getLogger(__name__)

investigate_router = Router()


def _build_footer(tools_used: list[dict], total_tokens: int) -> str:
    parts = []

    if tools_used:
        names = [t["name"] for t in tools_used if isinstance(t, dict)]
        counts = Counter(names)
        tools_str = " · ".join(f"`{name} ×{count}`" for name, count in counts.items())
        parts.append(f"🛠 {tools_str}")

    if total_tokens:
        parts.append(f"📊 `{total_tokens}` tokens")

    return "\n".join(parts) if parts else ""


def _build_response(data: dict) -> str:
    result = data.get("result") or ""
    footer = _build_footer(data.get("tools_used", []), data.get("total_tokens", 0))

    if footer:
        return f"{result}\n\n——————————\n{footer}"
    return result


@investigate_router.message()
async def investigate_handler(message: Message) -> None:
    target = message.text
    if not target:
        return

    status_msg = await message.answer("_Расследование запущено..._")

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{config.api_url}/api/investigate",
                json={"target": target, "max_tokens": config.max_tokens},
                timeout=120.0,
            )
            resp.raise_for_status()

        data = resp.json()
        await status_msg.edit_text(_build_response(data), parse_mode="HTML")

    except httpx.HTTPStatusError as e:
        logger.error("API error %s: %s", e.response.status_code, e.response.text)
        await status_msg.edit_text(f"❌ Ошибка API: `{e.response.status_code}`")

    except httpx.RequestError as e:
        logger.error("Request failed: %s", e)
        await status_msg.edit_text("❌ Сервер расследований недоступен.")
