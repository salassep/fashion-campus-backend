from flask import Blueprint, abort, request
from model.models import Base
from util.db import get_engine
from util.populate import populate_data

helper_func_bp = Blueprint("helper_func", __name__, url_prefix="")

@helper_func_bp.route("/helper-drop", methods=["GET"])
def drop_table():
    engine = get_engine() 
    Base.metadata.drop_all(engine)
    return {"success": True}
    
@helper_func_bp.route("/helper-insert", methods=["GET"])
def insert_data():
    populate_data()
    return {"success": True}
