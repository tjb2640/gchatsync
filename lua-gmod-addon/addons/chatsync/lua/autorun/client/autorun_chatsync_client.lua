local discord_tag_color = Color(255, 255, 255)
local username_color = Color(255, 255, 255)
local discriminator_color = Color(255, 255, 255)
local message_color = Color(255, 255, 255)

local add_message_to_chat = function(message)
    if message then 
        chat.AddText(
            discord_tag_color, "[DC] ",
            username_color, message.username,
            discriminator_color, "#", message.discriminator, ": ",
            message_color, message.content,
            color_white, "\n"
        )
    end
end

net.Receive("chatsync_broadcast_messages", function(len)
    local messages = util.JSONToTable(util.Decompress(net.ReadString()))
    for i = 1, #messages do
        add_message_to_chat(messages[i])
    end
end)