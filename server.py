import os
import random

from flask import Flask, jsonify
from flask import redirect
from flask import send_from_directory
from flask import url_for

from ezhue import HueColors
from util import thread_it

static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
print(static_folder, os.getcwd(), os.path.dirname(os.path.realpath(__file__)))
app = Flask("dreammachine", static_folder=static_folder)
dream_machine = None

@app.route("/state")
def state():
    return jsonify(playing=dream_machine.chrome_cast.playing, hue_on=dream_machine.hue.on)

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
        text-transform: lowercase;
    }

    h4 {
        font-size: normal;
    }

    a .button {
        padding-top:20px;
        padding-bottom: 20px;
    }

    .button:active {
        background-color: cyan;
    }
    .disco-santa-clause {
      animation: colorchange 50s; /* animation-name followed by duration in seconds*/

    }

    .nest {
        margin: auto;
        width: auto;
        border: solid 1px #ececec;
        border-radius: 5px;
        margin-bottom: 10px;
        margin-top: 10px;
        background-color: #fafafa;
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
        float: left;
        font-size: 22pt;
        text-align: center;
        width: 35%;
        padding: 2%;
        margin: 5%;
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
               ("disco-santa-claus", "Disco Santa Claus"),
               ("chrome-cast", nprMsg(dream_machine.chrome_cast.playing)),
               ("colder", "Cool It Down"),
               ("hotter", "I'm Chilly!"),
               ("fan-on", "I CAN'T BREATHE!"),
               ("zen-garden", "ZzzzzzzZzzZzz"),
               ]
    buttons = ''.join(
        map(lambda i: "<button onclick=\"post('" + i[0] + "')\" class=\"" + i[0] + " u-full-width button\">" + i[
            1] + "</button>",
            options))
    random_text = ["All🔘Your🔘Button🔘Pressing🔘Needs",
                   "THE HOMER ❤️'s YOU",
                   "i still think of myself as the homer",
                   "doh!",
                   "hello world!",
                   "💖",
                   "not related to the OA 👼🏻",
                   "Dream a Little Dream Of Me 😙",
                   "🐈🐈🐈🐈 🐈 🐈 🐈 🐈 🐈 🐈 🐈 🐈 🐈 🐈"]
    return """
    <!DOCTYPE html>
    <meta charset=utf-8>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name=apple-mobile-web-app-capable content=yes>
    <meta name=apple-mobile-web-app-status-bar-style content=white>
    <title>dream machine</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fetch/2.0.2/fetch.min.js"></script>
    <script>
        function post(url) {
            fetch(url, {
              method: 'POST',
            }).then(r => document.location.reload(true));
        }
    </script>
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


@app.route("/toggle-hue",  methods=['POST'])
def toggle_lights():
    dream_machine.toggle_lights()
    return "", 204


@app.route("/disco-santa-claus", methods=['POST'])
def disco():
    ensure_on(lambda: dream_machine.hue.disco_santa_claus())
    return "", 204


@app.route("/blue", methods=['POST'])
def blue():
    ensure_on(lambda: dream_machine.hue.set_color(HueColors.Blue))
    return "", 204


@app.route("/chrome-cast", methods=['POST'])
def toggle_chromecast():
    dream_machine.toggle_chromecast()
    return "", 204

@app.route("/random-color", methods=['POST'])
def random_color():
    ensure_on(lambda: dream_machine.hue.make_lights_rando())
    return True


@app.route("/fan-on", methods=['POST'])
def fan_on():
    dream_machine.nest.fan_on()
    return True


@app.route("/colder", methods=['POST'])
def colder():
    dream_machine.nest.colder()
    return "", 204


@app.route("/hotter", methods=['POST'])
def hotter():
    dream_machine.nest.hotter()
    return "", 204


@app.route("/zen-garden", methods=['POST'])
def zen():
    dream_machine.take_me_to_the_zen_garden()
    return "", 204


def run(dm):
    global dream_machine
    dream_machine = dm
    app.run(host='0.0.0.0', port=80)
