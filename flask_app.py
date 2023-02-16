from flask import Flask, request

from teapot import *

# teapot app

app = Flask(__name__)
teapot: Teapot | None = None


@app.route('/api/create')
def create_teapot():
    global teapot
    if teapot is not None:
        return 'Teapot already exists, reset it first with /reset'
    teapot = Teapot()
    # return message that tells that teapot created
    return 'Teapot created'


def is_float(s: str):
    try:
        float(s)
        return True
    except ValueError:
        return False


@app.route('/api/fill')
def fill_teapot():
    global teapot
    if teapot is None:
        return 'Teapot does not exist, create it first with /create'

    args = request.args

    if 'water_level' not in args or not is_float(args['water_level']):
        return 'Water level is not specified or is not float'
    water_level = float(args['water_level'])
    if 'water_temp' not in args or not is_float(args['water_level']):
        water_temp = 20
    else:
        water_temp = float(args['water_temp'])

    _, msg = teapot.set_water_level(water_level, water_temp)

    return msg


@app.route('/api/start_boiling')
def start_boiling():
    global teapot
    if teapot is None:
        return 'Teapot does not exist, create it first with /create'
    if teapot.water_level == 0:
        return 'Teapot is empty, fill it first with /fill'
    _, msg = teapot.start_boiling()
    return msg


@app.route('/api/stop_boiling')
def stop_boiling():
    global teapot
    if teapot is None:
        return 'Teapot does not exist, create it first with /create'

    _, msg = teapot.stop_boiling()
    return msg


@app.route('/api/status')
def status():
    global teapot
    if teapot is None:
        return 'Teapot does not exist, create it first with /create'

    return teapot.__str__()


@app.route('/reset')
def reset():
    global teapot
    teapot = None
    return 'Teapot reset'


if __name__ == '__main__':
    app.run()
