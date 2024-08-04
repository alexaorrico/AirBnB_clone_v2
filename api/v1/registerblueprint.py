from flask import Flask
from blueprint  import simple_page

app = Flask(__name__)
#app.register_blueprint(simple_page)
app.register_blueprint(simple_page, url_prefix='/pages')
