<<<<<<< HEAD
=======
#!/usr/bin/python3
""" """


from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

app_views = Blueprint("simple_page", __name__, tamplate_folder='tamplates')

@simple_page.route("/api/v1")
def index():
<<<<<<< HEAD
    pass
>>>>>>> refs/remotes/origin/storage_get_count
=======
    pass
>>>>>>> refs/remotes/origin/storage_get_count
