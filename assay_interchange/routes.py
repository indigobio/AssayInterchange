from assay_interchange import app
from flask import request
from assay_interchange.lib import convert_data


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/', methods=['POST'])
def index_post():
    return convert_data(request)


@app.route('/convert', methods=['POST'])
def convert():
    return convert_data(request)