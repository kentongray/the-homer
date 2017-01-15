import random

from flask import Flask
from flask import redirect
from flask import url_for

from ezhue import HueColors

app = Flask("dreammachine")
dream_machine = None


def on_off(val):
    if not val:
        return "On"
    else:
        return "Off"


style = """
  <style>
    .disco-santa-clause {
      animation: colorchange 50s; /* animation-name followed by duration in seconds*/

    }

    @keyframes colorchange {
      0%   {background: cyan;}
      25%  {background: yellow;}
      50%  {background: blue; color: white;}
      75%  {background: green;}
      100% {background: cyan;}
    }

    </style>
    """


@app.route("/")
def index():
    options = [("toggle-hue", "Hue " + on_off(dream_machine.hue.on)),
               ("random-color", "I'm Feeling Random"),
               ("blue", "A Little Blue"),
               ("disco-santa-clause", "Disco Santa Clause"),
               ("chrome-cast", "ChromeCast " + on_off(dream_machine.chrome_cast.playing))]
    buttons = ''.join(
        map(lambda i: "<a href=\"" + i[0] + "\" class=\"" + i[0] + " u-full-width button\">" + i[1] + "</a>",
            options))
    random_text = ["All🔘Your🔘Button🔘Pressing🔘Needs",
                   "DREAM MACHINE ❤️s YOU",
                   "💖",
                   "Dream a Little Dream Of Me 😙",
                   "🐈 🐈 🐈 🐈 🐈 🐈 🐈 🐈 🐈 🐈 🐈"]
    return """
    <!DOCTYPE html>
    <meta charset=utf-8>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name=apple-mobile-web-app-capable content=yes>
    <meta name=apple-mobile-web-app-status-bar-style content=white>
    <title>Dream Machine</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css" />
    <h1 style=\"text-transform:uppercase\">DreamMachine</h2>
    %s
    <h4>%s</h4>
    <link href="https://afeld.github.io/emoji-css/emoji.css" rel="stylesheet">

    %s
    """ % (style, random.choice(random_text), buttons)


@app.route("/toggle-hue")
def toggle_lights():
    dream_machine.toggle_lights()
    return redirect(url_for('index'))


@app.route("/disco-santa-clause")
def disco():
    dream_machine.hue.toggle(True)
    dream_machine.hue.disco_santaclause()
    return redirect(url_for('index'))


@app.route("/blue")
def blue():
    dream_machine.hue.toggle(True)
    dream_machine.hue.set_color(HueColors.Blue)
    return redirect(url_for('index'))


@app.route("/chrome-cast")
def toggle_chromecast():
    dream_machine.toggle_chromecast()
    return redirect(url_for('index'))


@app.route("/random-color")
def random_color():
    dream_machine.hue.toggle(True)
    dream_machine.hue.make_lights_rando()
    return redirect(url_for('index'))


def run(dm):
    global dream_machine
    dream_machine = dm
    app.run(host='0.0.0.0', port=80)
