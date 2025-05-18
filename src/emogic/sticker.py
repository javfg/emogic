import asyncio
import json

import aiofiles
import aiohttp
from loguru import logger
from telegram.ext import ContextTypes

from emogic.config import config


class StickerUploader:
    def __init__(self) -> None:
        self.dump_group_ids = config.dump_group_ids
        self.next = 0
        self.file_id_cache: dict[str, str] = {}
        logger.debug(f"sticker uploader instance created, {len(self.dump_group_ids)} dump groups")

    async def _dump_group_id(self) -> str:
        current = self.dump_group_ids[self.next]
        self.next += 1
        if self.next >= len(self.dump_group_ids):
            await asyncio.sleep(2)  # 20 messages per minute per group limit
            self.next = 0
        return current

    async def flush_file_id_cache(self) -> None:
        logger.debug("flushing file_id cache")
        f = await aiofiles.open(config.sticker_data_path, "a")
        for emoji_description, file_id in self.file_id_cache.items():
            await f.write(f"{json.dumps({emoji_description: file_id})}\n")
        await f.close()
        logger.debug(f"written {len(self.file_id_cache)} sticker file_ids")
        self.file_id_cache = {}

    async def store_file_id(self, emoji_codepoint: str, file_id: str) -> None:
        self.file_id_cache[emoji_codepoint] = file_id
        if len(self.file_id_cache) > config.sticker_cache_size:
            await self.flush_file_id_cache()

    async def upload_sticker(
        self,
        context: ContextTypes.DEFAULT_TYPE,
        sticker_url: str,
        emoji_description: str,
    ) -> str | None:
        next_dump_group_id = await self._dump_group_id()
        logger.trace(f"uploading sticker to dump group {next_dump_group_id}")

        async with aiohttp.ClientSession() as session:
            async with session.get(sticker_url) as response:
                sticker_bytes = await response.read()
                message = await context.bot.send_sticker(chat_id=next_dump_group_id, sticker=sticker_bytes)
                if not message.sticker:
                    logger.error("failed to upload sticker")
                    return

                file_id = message.sticker.file_id
                await self.store_file_id(emoji_description, file_id)

                return file_id


sticker_uploader = StickerUploader()
