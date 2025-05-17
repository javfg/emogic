# Emogic bot
Send an emoji or two to the bot and explore! :robot: :rocket:

# Usage
1. Create a bot using [@BotFather](https://t.me/botfather) and get the token.
2. Enable the bot's inline mode in the bot settings.
3. Download metadata.json from [here](https://github.com/xsalazar/emoji-kitchen-backend/blob/main/app/metadata.json):
    ```bash
    mkdir -p metadata
    curl -o metadata/metadata.json https://raw.githubusercontent.com/xsalazar/emoji-kitchen-backend/main/app/metadata.json
    ```
    and place it in `./metadata/metadata.json`.
4. Fill .env file:
    ```bash
    cat > .env << EOF
    EMOGIC_TOKEN="${bot_token}"
    EMOGIC_METADATA_PATH="./metadata/metadata.json"
    EOF
    ```
5. Run the bot:
    ```bash
      docker-compose up -d
    ```
6. Invoke the bot with `@{bot_name}` and send an emoji or two.
