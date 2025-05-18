import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger


def must_str(env_var: str) -> str:
    value = os.environ.get(env_var)
    if value is None:
        raise ValueError(f"missing required environment variable {env_var}")
    return value


def must_path(env_var: str) -> Path:
    return Path(must_str(env_var)).absolute()


def must_list(env_var: str) -> list[str]:
    return must_str(env_var).split(" ")


class Config:
    def __init__(self):
        logger.debug("loading config")
        load_dotenv()

        self.token = must_str("EMOGIC_TOKEN")
        self.dump_group_ids = must_list("EMOGIC_DUMP_GROUP_IDS")
        self.emoji_data_path = must_path("EMOGIC_DATA_PATH") / "emoji.json"
        self.sticker_data_path = must_path("EMOGIC_DATA_PATH") / "ids.ndjson"
        log_level = os.environ.get("EMOGIC_LOG_LEVEL", "INFO")
        self.sticker_cache_size = int(os.environ.get("EMOGIC_STICKER_CACHE_SIZE", 0))

        logger.remove()
        logger.add(sink=sys.stderr, level=log_level)

        self.validate()

        # graceful shutdown with

    def validate(self):
        if not self.emoji_data_path.exists():
            raise ValueError(f"emoji.json not found in {self.emoji_data_path}")

        if not self.sticker_data_path.exists():
            logger.info(f"ids file {self.sticker_data_path} does not exist, creating")
            self.sticker_data_path.touch()


config = Config()
