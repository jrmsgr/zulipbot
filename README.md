# zulipbot
Use Zulip to control the world.

## Rationale

This robot implements commands that the user can trigger on the Zulip chat.  
Those commands do things such as:
  - printing posts, pics, gifs from Reddit
  - playing music from Reddit
  - playing music from Youtube
  - making jokes
  - giving you a weather report

## Requirements

### Python Packages
Requires Python >= 3.9.
```shell
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```
### Progams
  - **cvlc**: audio/video player
  - **pulseaudio**: manages volume and audio outputs

### Setup Files
Add the following files in this directory:
  - **zuliprc**, used by Zulip's client. Create a bot in Zulip
    (*Personal settings > Bots > Add a new bot*, type "Generic bot"), then download its zuliprc.
    See [Zulip documentation](https://zulip.com/api/running-bots). It looks like:
    ```
    [api]
    email=mybot-bot@myorg.zulipchat.com
    key=<BOT_API_KEY>
    site=https://myorg.zulipchat.com
    ```
    The bot must be subscribed to the channels it should listen to.
  - **msg_filters.json**, a list of filters selecting the Zulip messages the bot responds to.
    A message is accepted if it matches all the keys of at least one filter.
    Besides raw Zulip message fields, the keys `channel`, `topic` and `type`
    (`channel` or `direct`) are supported:
    ```
    [
        {"channel": "MyChannel"},
        {"type": "direct"}
    ]
    ```
  - **praw.ini** (optional), used by Reddit's client. Without it, reddit commands are disabled.
    See [praw documentation](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html)

## Usage
```shell
./venv/bin/python main.py   # or ./run.sh to run it in the background
```
Then, in Zulip, type:
```
!help
```

## Acknowledgements

Thanks to my buddy T3lchar for letting me steal his bot: https://github.com/T3lchar/zulip_bot

## FAQ

Q: The command **!weather** fails with an SSL error, what's wrong?  
A: Take a look at this [issue](https://stackoverflow.com/questions/44649449/brew-installation-of-python-3-6-1-ssl-certificate-verify-failed-certificate/44649450#44649450) and execute ./bin/install_certifi.py
