import json

from loguru import logger

from emogic.config import config
from emogic.emoji import Emoji, EmojiCombination


class EmojiManager:
    def __init__(self):
        self.emojis: dict[str, Emoji] = {}
        self.combination_count = 0

        sticker_data_lines = config.sticker_data_path.read_text().splitlines()
        sticker_dict = {k: v for line in sticker_data_lines for k, v in json.loads(line).items()}
        logger.info(f"loaded {len(sticker_dict)} file ids")

        emoji_dict = json.loads(config.emoji_data_path.read_text())

        for data_codepoint, emoji_data in emoji_dict["data"].items():
            self.emojis[data_codepoint] = Emoji(
                codepoint=data_codepoint,
                description=emoji_data["alt"],
                combinations={},
            )
        logger.info(f"loaded {len(self.emojis)} emojis")

        for codepoint, emoji in self.emojis.items():
            data_combinations_dict = emoji_dict["data"][codepoint]["combinations"]

            for data_codepoint, data_combinations_list in data_combinations_dict.items():
                e = data_combinations_list[0]  # we ignore the rest of emojis in combinations list
                emoji.combinations[data_codepoint] = EmojiCombination(
                    url=e["gStaticUrl"],
                    description=e["alt"],
                    left_emoji=self.emojis[e["leftEmojiCodepoint"]],
                    right_emoji=self.emojis[e["rightEmojiCodepoint"]],
                    file_id=sticker_dict.get(e["alt"]),
                )
                self.combination_count += 1
        logger.info(f"loaded {self.combination_count} combinations")

    def get_emoji_by_codepoint_sequence(self, codepoint_sequence: str) -> Emoji | None:
        return self.emojis.get(codepoint_sequence, self.emojis.get(codepoint_sequence.split("-")[0]))


emoji_manager = EmojiManager()
