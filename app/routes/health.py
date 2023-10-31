from flask import Blueprint
from app.services.authorization import verify_token

dicom_health = Blueprint("dicom_health", __name__)

@dicom_health.route("/health", methods=["GET"])
@verify_token
def health():
    return {"health": "Ok"}, 200

