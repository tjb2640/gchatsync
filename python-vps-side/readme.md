# Chat sync - python portion

## Make a Discord bot
Create a Discord bot on the Discord bot dash website or whatever. Make sure it is a private bot (don't flip the public bot switch).

Invite it to your server by placing its **Client ID** in place of the asterisks in this URL: `https://discord.com/api/oauth2/authorize?client_id=*****************&permissions=1024&scope=bot%20applications.commands` then navigate to the URL in your web browser.

## Modify bot.py
`bot.py` runs the Discord bot. Make sure the user running `bot.py` has read/write permissions in the directory.

Modify `bot.py` (this is the Discord bot code):
- `discord_bot_token` should contain your Discord bot's token. **THIS IS A PRIVATE KEY, do NOT commit it or share it ANYWHERE.**
- Copy the ID of the Discord channels you want to sync chat from. Key them into `channel_id_messages` as an empty array (`[]`) and `channel_id_to_server_name` with a string containing a meaningful server name like 'east' or 'west' for instance. *(User known as "fard", I did this step for you already.)*

## Modify getter.py
Modify `getter.py` (this is the HTTP server):
- Modify `PORT` to something other than `8080` if you so desire (if the HTTP server runs on a separate machine from the game server, this will have to be something that is opened to external connections)
- Modify `api_keys`. The server names you came up with for `channel_id_to_server_name` in `bot.py` should be the values in the dict, and the keys should be some random ASCII API key that each server will use as a rudimentary auth token. Once again, these are to be treated as **private keys** and not shared with anyone.

## Remember the API keys for each server
When you configure the Lua addon for each Garry's Mod server you will need to remember the API keys for each server you install it to.

## Run the bot and the HTTP server
Make sure you also install `discord` and `fastapi` via `pip` (might be aliased to `pip3` on your system if `pip` doesn't exist)
```python
# Shell or screen 1
python3 bot.py
# Shell or screen 2
python3 getter.py
```