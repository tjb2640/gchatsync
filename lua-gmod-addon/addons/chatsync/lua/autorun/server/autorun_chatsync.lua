local MY_API_KEY = "place_servers_token_here_please"
local CHECK_INTERVAL = 5 -- seconds
local HTTP_SERVER_URL = "http://localhost:8000"




local timer = timer
local net = net
local RealTime = RealTime

util.AddNetworkString("chatsync_broadcast_messages")
local timer_id_pulldown = "chatsync_pulldown"
local timer_id_check = "chatsync_healthcheck"

local broadcast_messages = function(messages)
    net.Start("chatsync_broadcast_messages")
        net.WriteString(util.Compress(util.TableToJSON(messages)))
    net.Broadcast()
end

local last_check = RealTime()
local async_get_new_messages = function()
    local full_url = string.format("%s/egress?token=%s", HTTP_SERVER_URL, MY_API_KEY)
    http.Fetch(full_url,
        -- success
        function(body, len, headers, code)
            local messages = util.JSONToTable(body)
            broadcast_messages(messages)
        end,
        -- failure
        function(msg)
            print("CHATSYNC PROBLEM: " .. (msg or "no message"))
        end,
    )
end

-- creates timer that fetches messages from the server
local create_pulldown_timer = function()
    timer.Create(timer_id_pulldown, CHECK_INTERVAL, 0, function()
        async_get_new_messages()
        last_check = RealTime()
    end)
end

-- if chatsync is suddenly not alive, recreate the timer and start syncing again
local create_check_timer = function()
    timer.Create(timer_id_check, 30, 0, function()
        if RealTime() > last_check + (CHECK_INTERVAL * 3) then
            create_pulldown_timer()
        end
    end)
end

hook.Add("InitPostEntity", "IPE_CreateChatSyncPipeline", function()
    last_check = RealTime()
    create_pulldown_timer()
    create_check_timer()
end)