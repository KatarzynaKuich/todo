
from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

from views import *

if __name__ == "__main__":
    app.run(debug=True)


