# Emogic bot
Send an emoji or two to the bot and explore! :robot: :rocket:

# Usage
1. Create a bot using [@BotFather](https://t.me/botfather) and get the token.
2. Enable the bot's inline mode and privacy mode in the bot settings.
3. Create some dump channels, invite the bot to them, and get their IDs.
4. Download metadata.json from [emoji-kitchen](https://github.com/xsalazar/emoji-kitchen):
    ```bash
    mkdir -p metadata
    curl -o metadata/metadata.json https://raw.githubusercontent.com/xsalazar/emoji-kitchen-backend/main/app/metadata.json
    ```
    and place it in `./metadata/emoji.json`.
5. Fill .env file:
    ```bash
    cat > .env << EOF
    EMOGIC_TOKEN="${bot_token}"
    EMOGIC_DUMP_GROUP_IDS="${group_id_1} ${group_id_2}"
    EMOGIC_DATA_PATH="./metadata"
    EMOGIC_LOG_PATH="./logs"
    EMOGIC_LOG_LEVEL="DEBUG"
    EMOGIC_STICKER_CACHE_SIZE=100
    EMOGIC_UID=17000
    EMOGIC_GID=17000
    EOF
    ```
6. Run the bot:
    ```bash
      docker-compose up -d
    ```
7. Invoke the bot with `@{bot_name}` and send an emoji or two.

Emoji suggestion fetching is flaky, as it has to upload a sticker to Telegram
for each. Performance should improve as you get your ID table built.
