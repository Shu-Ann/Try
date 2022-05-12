from flask import Flask
from controller.index_controller import index_page

app = Flask(__name__)

app.register_blueprint(index_page, url_prefix="/")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug=True)

