"""handles import initialization"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, template_folder="templates", url_prefix="/api/v1")


