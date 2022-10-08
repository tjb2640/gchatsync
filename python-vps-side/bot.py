# https://discord.com/api/oauth2/authorize?client_id=*****************&permissions=1024&scope=bot%20applications.commands
import discord
import os
from os.path import exists
import json

discord_bot_token = 'YOUR_BOT_TOKEN_HERE'
savedir = 'fakedb'
channel_id_messages = {
    709462881367752754: [],
    709482207839912008: [],
}
channel_id_to_server_name = {
    709462881367752754: 'east',
    709482207839912008: 'west',
}





intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

try:
    os.mkdir(savedir, 0o640)
except OSError as error: # exists
    pass

# Simple for now but you might consider other messages to be "empty" (read: skippable/garbage)
def is_empty(content):
    return not content

# TODO: you should determine what stuff you need to strip out of the message
# to make sure people can't overload whatever addon chatbox you're using
def sanitize_for_game_chat(content: str) -> str:
    return content.encode('ascii', 'ignore').decode()

def store_messages_for_channel(channelid: int):
    if channelid in channel_id_messages.keys():
        msgs_json = json.dumps(channel_id_messages[channelid])
        fname = '%s/%s' % (savedir, channel_id_to_server_name[channelid])
        fname_tmp = '%stmp' % fname
        # keep it atomic so getter.py doesn't fight with our data:
        with open(fname_tmp, 'w') as f:
            f.write(msgs_json)
            f.flush()
            os.sync()
        os.replace(fname_tmp, fname)

def clear_egressed_messages(channelid: int):
    if channelid in channel_id_messages.keys():
        fname = '%s/%s' % (savedir, channel_id_to_server_name[channelid])
        if not exists(fname):
            channel_id_messages[channelid].clear()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id in channel_id_messages.keys():
        content = sanitize_for_game_chat(message.content)
        if not is_empty(content):
            clear_egressed_messages(message.channel.id)
            channel_id_messages[message.channel.id].append({
                'username': sanitize_for_game_chat(message.author.display_name),
                'discriminator': str(message.author.discriminator),
                'content': content
            })
            store_messages_for_channel(message.channel.id)
            print('[MSG/%s] %s#%s: %s' % (channel_id_to_server_name[message.channel.id],
                message.author.display_name, message.author.discriminator, message.content))

if __name__ == '__main__':
    print('Starting bot')
    client.run(discord_bot_token)
    