import random

from flask import Flask
from flask import redirect
from flask import url_for

from ezhue import HueColors
from util import thread_it

app = Flask("dreammachine")
dream_machine = None


def on_off(val):
    if not val:
        return "On"
    else:
        return "Off"


def nprMsg(val):
    if not val:
        return "NPR Me"
    else:
        return "That's Enough NPR"


style = """
  <style>

    h1, h2, h3, h4, .random {
        color: silver;
    }

    h4 {
        font-size: normal;
    }

    a .button {
        padding-top:20px;
        padding-bottom: 20px;
    }
    .disco-santa-clause {
      animation: colorchange 50s; /* animation-name followed by duration in seconds*/

    }

    .nest {
        margin: auto;
        width: auto;

    }

    .clear {
        clear: both;
    }

    .target-temperature {
        text-transform: uppercase;
        font-size: 10pt;
        text-align: center;
        margin-bottom: 3%;
        color: silver;
    }

    .inside-temperature, .outside-temperature {
        height: 50px;
        float: left;
        font-size: 18pt;
        text-align: center;
        width: 35%;
        padding: 2%;
        margin: 5%;
        border: solid 1px silver;
        border-radius: 5px;
        color: gray;
    }

    .inside-temperature::after, .outside-temperature::after {
        margin-top: -5px;
        display: block;
        color: silver;
        text-transform: uppercase;
        font-size: 10pt;
     }

    .inside-temperature::after {
        content: "Inside";
    }

    .outside-temperature::after {
        content: "Outside";
    }
    .blue {
        background-color: rgb(145, 220, 255);
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


def nest_html():
    return """
        <div class="nest">
            <div class="inside-temperature">
                %s°
            </div>
            <div class="outside-temperature">
                %s°
            </div>
            <div class="clear"></div>
            <div class="target-temperature">Target %s°</div>
        </div>
        """ % (dream_machine.nest.inside_temperature, dream_machine.nest.outside_temperature, dream_machine.nest.target)


@app.route("/")
def index():
    options = [("toggle-hue", "Hue " + on_off(dream_machine.hue.on)),
               ("random-color", "I'm Feeling Random"),
               ("blue", "A Little Blue"),
               ("disco-santa-clause", "Disco Santa Clause"),
               ("chrome-cast", nprMsg(dream_machine.chrome_cast.playing)),
               ("colder", "Cool It Down"),
               ("hotter", "I'm Chilly!"),
               ("fan-on", "I CAN'T BREATH!"),
               ]
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
    <title>DreamMachine</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css" />
    <h1 style=\"text-transform:lowercase\">DreamMachine</h2>
    %s
    <div class="random">%s</div>
    <div>
        %s
    </div>
    %s
    """ % (style, random.choice(random_text), nest_html(), buttons)


def redirect_async(action):
    thread_it(action)
    return redirect(url_for('index'))


def ensure_on(func):
    def callback():
        dream_machine.hue.toggle(True)
        func()

    return callback


@app.route("/toggle-hue")
def toggle_lights():
    return redirect_async(lambda: dream_machine.toggle_lights())


@app.route("/disco-santa-clause")
def disco():
    return redirect_async(ensure_on(lambda: dream_machine.hue.disco_santa_clause()))


@app.route("/blue")
def blue():
    return redirect_async(ensure_on(lambda: dream_machine.hue.set_color(HueColors.Blue)))


@app.route("/chrome-cast")
def toggle_chromecast():
    return redirect_async(lambda: dream_machine.toggle_chromecast())


@app.route("/random-color")
def random_color():
    return redirect_async(ensure_on(lambda: dream_machine.hue.make_lights_rando()))


@app.route("/fan-on")
def fan_on():
    return redirect_async(ensure_on(lambda: dream_machine.nest.fan_on()))


@app.route("/colder")
def colder():
    return redirect_async(ensure_on(lambda: dream_machine.nest.colder()))

@app.route("/hotter")
def hotter():
    return redirect_async(ensure_on(lambda: dream_machine.nest.hotter()))

def run(dm):
    global dream_machine
    dream_machine = dm
    app.run(host='0.0.0.0', port=80)
