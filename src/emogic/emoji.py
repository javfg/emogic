from __future__ import annotations

from dataclasses import dataclass

from loguru import logger
from telegram import InlineQueryResultCachedSticker
from telegram.ext import ContextTypes

from emogic.sticker import sticker_uploader


@dataclass
class Emoji:
    codepoint: str
    description: str
    combinations: dict[str, EmojiCombination]

    def get_combination_with(self, right_emoji: Emoji) -> EmojiCombination | None:
        return self.combinations.get(right_emoji.codepoint)


@dataclass
class EmojiCombination:
    url: str
    description: str
    left_emoji: Emoji
    right_emoji: Emoji
    file_id: str | None

    async def as_sticker(self, context: ContextTypes.DEFAULT_TYPE) -> InlineQueryResultCachedSticker | None:
        if not self.file_id:
            logger.trace(f"file_id not found for {self.description}, uploading sticker")
            self.file_id = await sticker_uploader.upload_sticker(context, self.url, self.description)
            if not self.file_id:
                logger.error("failed to upload sticker")
                return

        return InlineQueryResultCachedSticker(
            id=f"{self.left_emoji.codepoint}-{self.right_emoji.codepoint}-{id(self)}",
            sticker_file_id=self.file_id,
        )
