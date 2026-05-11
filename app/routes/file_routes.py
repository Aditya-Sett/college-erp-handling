from flask import Blueprint, send_from_directory, abort
import os

file_bp = Blueprint("file", __name__)

UPLOAD_FOLDER = "../uploads"


@file_bp.route("/files/<filename>", methods=["GET"])
def get_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        abort(404)