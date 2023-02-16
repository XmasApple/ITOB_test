import logging

from flask import Flask, request, Response

from teapot import Teapot

app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True
teapot: Teapot | None = None


@app.route('/api/create')
def create_teapot():
    global teapot
    if teapot is not None:
        return Response(
            'Teapot already exists, reset it first with /reset', status=400)

    teapot = Teapot()

    return Response('Teapot created', status=201)


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
        return Response(
            'Teapot does not exist, create it first with /create', status=400)

    args = request.args

    if 'water_level' not in args or not is_float(args['water_level']):
        return Response(
            'Water level is not specified or is not float', status=400)

    water_level = float(args['water_level'])
    if 'water_temp' not in args or not is_float(args['water_level']):
        water_temp = 20
    else:
        water_temp = float(args['water_temp'])

    is_set, msg = teapot.set_water_level(water_level, water_temp)

    return Response(msg, status=200 if is_set else 400)


@app.route('/api/start_boiling')
def start_boiling():
    global teapot
    if teapot is None:
        return Response(
            'Teapot does not exist, create it first with /create', status=400)

    if teapot.water_level == 0:
        return Response('Teapot is empty, fill it first with /fill')

    is_started, msg = teapot.start_boiling()

    return Response(msg, status=200 if is_started else 400)


@app.route('/api/stop_boiling')
def stop_boiling():
    global teapot
    if teapot is None:
        return Response(
            'Teapot does not exist, create it first with /create', status=400)

    _, msg = teapot.stop_boiling()
    return msg


@app.route('/api/status')
def status():
    global teapot
    if teapot is None:
        return Response(
            'Teapot does not exist, create it first with /create', status=400)

    return Response(str(teapot))


@app.route('/reset')
def reset():
    global teapot
    teapot = None
    return Response('Teapot reset')


if __name__ == '__main__':
    app.run()
