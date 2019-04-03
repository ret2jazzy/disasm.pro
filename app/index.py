from . import asm_ninja
from flask import send_from_directory

@asm_ninja.route("/", methods=['GET'])
def index():
    return send_from_directory('index', 'index.html')
