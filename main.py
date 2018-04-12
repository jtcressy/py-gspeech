from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return f"Hello, World! TypeOf(int): {type(int)}"


if __name__ == '__main__':
    app.run()
