from weppy import App

app = App(__name__)  # pylint: disable=C0103


@app.route("/")
def hello():
    return "Hello WEPPY!"
