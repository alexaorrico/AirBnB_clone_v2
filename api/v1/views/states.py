from models.base_model import BaseModel, Base
from flask import jsonify
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'])
def allstates():
    """ jsonify """
    lista = []
    for i in storage.all(State):
        j = i.BaseModel.to_dict()
        lista.append(j)
    return (lista)
