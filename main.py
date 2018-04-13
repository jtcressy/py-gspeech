from flask import Flask, request, render_template
import gspeech
import sys, logging
from os import environ
app = Flask(__name__)


@app.route('/')
def hello_world():
    return f"Hello World, {__name__}"


@app.route('/transcribe', methods=['GET', 'POST'])
def transcribe_audio():
    import json
    logger = logger_setup()
    print("transcribe")
    if request.method == 'POST':
        print("transcribe start")
        file = request.files['file']
        samplerate = request.form.get('sampleRate', None)
        try:
            if samplerate:
                result = gspeech.process(file.read(), samplerate)
            else:
                result = gspeech.process(file.read())
        except Exception as e:
            result = str(e)
        logger.info("[POST]: file: {}; samplerate: {}; result: {}".format(file, samplerate, result))
        return ''.join([''.join([y.transcript for y in x.alternatives]) for x in result.results])
    else:
        return render_template('transcribe.html')


def logger_setup(log_name="csbot", log_level=logging.INFO):
    logger = logging.getLogger(log_name)
    loghandler = logging.StreamHandler(stream=sys.stdout)
    logfilehandler = logging.FileHandler(f"{log_name}.log", mode="a", encoding="utf-8")
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
    loghandler.setFormatter(formatter)
    logfilehandler.setFormatter(formatter)
    if len(logger.handlers) < 1:
        logger.addHandler(loghandler)
        logger.addHandler(logfilehandler)
    loglevels = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "WARN": logging.WARN,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }
    loglevel = loglevels.get(environ.get("LOGLEVEL", "INFO").upper(), log_level)
    logger.setLevel(loglevel)
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            logger.info(f"Logfile location: {handler.baseFilename}")
    return logger


if __name__ == '__main__':
    app.run(port='8080')
