module.exports = (robot) ->                                        
    robot.respond /give it to me/i, (res) ->
        attach = {
            "text": "Would you like to play a game?",
            "attachments": [
                {
                    "text": "Choose a game to play",
                    "fallback": "You are unable to choose a game",
                    "callback_id": "wopr_game",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                        {
                            "name": "game",
                            "text": "Chess",
                            "type": "button",
                            "value": "chess"
                        },
                        {
                            "name": "game",
                            "text": "Falken's Maze",
                            "type": "button",
                            "value": "maze"
                        },
                        {
                            "name": "game",
                            "text": "Thermonuclear War",
                            "style": "danger",
                            "type": "button",
                            "value": "war",
                            "confirm": {
                                "title": "Are you sure?",
                                "text": "Wouldn't you prefer a good game of chess?",
                                "ok_text": "Yes",
                                "dismiss_text": "No"
                            }
                        }
                    ]
                }
            ]
        };

        res.send attach


    robot.hear /createFile/i, (res) ->
        @exec = require('child_process').exec
        cmd = "ls -la"
        res.send "Start Command -> [#{cmd}]"
        @exec cmd, (error, stdout, stderr) ->
            if error
                res.send error
                res.send stderr
            else




