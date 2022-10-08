# Chat sync - GMod addon portion

## Modify the GMod addon
The core logic is located in `addons/chatsync/lua/autorun/[client|server]`.

In the client file (`autorun/client/autorun_chatsync_client.lua`), modify the color values that will be used when formatting the messages into chat.

Examine the `add_message_to_chat` function to see what is being formatted.

In the server file (`autorun/server/autorun_chatsync.lua`), modify the following:
- `MY_API_KEY` - **specific to the current server.** Should line up with the API keys you placed into python->getter.py.
- `CHECK_INTERVAL` - if you want to check for new messages every so often at an interval that isn't 5 seconds, I'd recommend you don't check any faster, but you could always check slower (>5) at the expense of latency.
- `HTTP_SERVER_URL` - URL to the HTTP server running in getter.py, **including the port, with no trailing slash.**

