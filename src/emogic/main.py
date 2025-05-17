import json
import os
import random
from pathlib import Path

import grapheme
from dotenv import load_dotenv
from loguru import logger
from telegram import InlineQueryResultPhoto, Update
from telegram.ext import ApplicationBuilder, ContextTypes, InlineQueryHandler


def build_result_photo(index: int, key: str | int, element: dict) -> InlineQueryResultPhoto:
    img = element.get("gStaticUrl", "")
    emojis = [element.get("leftEmoji"), element.get("rightEmoji")]
    caption = f"{element.get('alt')}, {emojis}"
    return InlineQueryResultPhoto(
        id=f"{key}-{index}",
        thumbnail_url=img,
        photo_url=img,
        caption=caption,
    )


async def emoji(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    # check if there is a query
    if not update.inline_query:
        return

    query = update.inline_query.query

    # check if the query contains a sane length
    if not query or len(query) > 20:
        return

    clusters = list(grapheme.graphemes(query))

    # check if the query contains one or two emoji
    if not clusters or len(clusters) > 2:
        return

    emoji_codepoints = []
    for cluster in clusters:
        if cluster:
            emoji_codepoints.append("-".join(format(ord(c), "x") for c in cluster))

    logger.info(f"emoji codepoints: {emoji_codepoints}")

    collection = metadata["data"].get(emoji_codepoints[0])
    if not collection:
        return

    if len(emoji_codepoints) == 1:
        # if there is only one emoji, return the list of combinations
        combinations = collection["combinations"]
        results = []

        for key, list_of_emojis in combinations.items():
            for index, element in enumerate(list_of_emojis):
                results.append(build_result_photo(index, key, element))

    elif len(emoji_codepoints) == 2:
        # if there are two emojis, return the combination
        combination_list = collection["combinations"].get(emoji_codepoints[1])

        if not combination_list:
            return

        results = [build_result_photo(index, 0, element) for index, element in enumerate(combination_list)]

    if update.inline_query:
        logger.info(f"found {len(results)} results for {query}")
        random.shuffle(results)
        await update.inline_query.answer(results=lambda x: results[x : x + 50], auto_pagination=True)


load_dotenv()

token = os.environ.get("EMOGIC_TOKEN")
if not token:
    raise ValueError("no token found in environment variables")

metadata_env_var = os.environ.get("EMOGIC_METADATA_PATH")
if not metadata_env_var:
    raise ValueError("no metadata path found in environment variables")
metadata_path = Path(metadata_env_var).absolute()

logger.info(f"loading metadata from {metadata_path}")
metadata = json.loads(metadata_path.read_text())

app = ApplicationBuilder().token(token).build()
app.add_handler(InlineQueryHandler(emoji))

logger.info("starting bot")
app.run_polling()
