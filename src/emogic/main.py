from random import shuffle

import grapheme
from loguru import logger
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, ContextTypes, InlineQueryHandler

from emogic.config import config
from emogic.emoji_manager import emoji_manager
from emogic.sticker import sticker_uploader
from emogic.util import anything, cs


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.inline_query or len(update.inline_query.query) > 20:
        return

    query = update.inline_query.query.replace(" ", "").replace(":", "")
    clusters = list(grapheme.graphemes(query))

    if not clusters or len(clusters) > 2:
        return

    codepoint_sequences = [cs(c) for c in clusters]
    logger.info(f"emoji codepoint sequences: {codepoint_sequences}")

    left_emoji = emoji_manager.get_emoji_by_codepoint_sequence(codepoint_sequences[0])
    if not left_emoji:
        return

    # if there is only one emoji, get the combinations for it
    if len(codepoint_sequences) == 1:
        offset = int(update.inline_query.offset or 0)
        batch_size = len(config.dump_group_ids)
        combinations = list(left_emoji.combinations.values())
        shuffle(combinations)
        stickers = anything([await c.as_sticker(context) for c in combinations[offset : offset + batch_size]])
        if not stickers:
            logger.info(f"no combinations found for {left_emoji.description}")
            return
        offset = offset + batch_size

        await update.inline_query.answer(stickers, next_offset=str(offset), cache_time=0)

    # if there are two emojis, get the combinations between them
    elif len(codepoint_sequences) == 2:
        right_emoji = emoji_manager.get_emoji_by_codepoint_sequence(codepoint_sequences[1])
        if not right_emoji:
            return
        combination = left_emoji.get_combination_with(right_emoji)
        if not combination:
            logger.info(f"combination not found for {left_emoji.description} and {right_emoji.description}")
            return
        sticker = await combination.as_sticker(context)
        if not sticker:
            logger.info(f"failed to create sticker for {left_emoji.description} and {right_emoji.description}")
            return

        await update.inline_query.answer([sticker])


def main():
    logger.info("starting bot")

    # graceful shutdown — write file_ids to file
    async def shutdown_handler(app: Application) -> None:
        logger.warning("shutting down gracefully")
        await sticker_uploader.flush_file_id_cache()

    app = ApplicationBuilder().write_timeout(240).post_shutdown(shutdown_handler).token(config.token).build()
    app.add_handler(InlineQueryHandler(handle))

    app.run_polling()
