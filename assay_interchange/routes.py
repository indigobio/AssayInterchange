from assay_interchange import app
from flask import request
from assay_interchange.lib import convert_data, validate_data


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/', methods=['POST'])
def index_post():
    return convert_data(request)


@app.route('/validate', methods=['POST'])
def validate():
    return validate_data(request)