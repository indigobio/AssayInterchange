import base64
import datetime
import json
import os
import traceback
import io
from dwarfsquad.lib.build import from_xlsx, from_json
from dwarfsquad.lib.build.from_json.helpers import build_full_ac_from_json
from dwarfsquad.lib.export.export_full_ac import get_workbook
from flask import make_response, jsonify
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook


def convert_data(request):
    try:
        file_store = request.files.values()[0]
        ac = get_ac(file_store)
        resp = make_response(get_output_file(ac, file_store), 200)
        filename = get_filename(ac) + get_output_format(file_store)
        resp.headers['Content-Disposition'] = "attachment; filename=" + filename
        resp.headers['Content-Type'] = get_application_type(get_output_format(file_store))
        resp.headers['filename'] = filename
        return resp
    except Exception as e:
        return make_response(build_error_response_message(e), 200)


def get_application_type(output_format):
    if output_format == '.xlsx':
        return 'application/vnd.ms-excel'
    elif output_format == '.json':
        return 'application/json'


def validate_data(request):
    file_store = request.files.values()[0]
    try:
        ac = get_ac(file_store)
        response_body = {
            'assay': ac.name,
            'format': os.path.splitext(file_store.filename)[1],
            'message': 'Success',
            'valid': True
        }

    except Exception as e:
        response_body = {
            'assay': None,
            'format': os.path.splitext(file_store.filename)[1],
            'message': build_error_response_message(e),
            'valid': False
        }
    return make_response(jsonify(response_body), 200)


def is_valid_xlsx_ac(file_store):
    try:
        assert file_store.filename.endswith('xlsx')
        file_store.stream.seek(0)
        wb = load_workbook(file_store.stream)
        from_xlsx.validate_workbook(wb)
        return True
    except:
        return False


def is_valid_json_ac(file_store):
    try:
        assert file_store.filename.endswith('json')
        file_store.stream.seek(0)
        json_data = json.load(file_store.stream)
        from_json.validate_json(json_data)
        return True
    except:
        return False


def is_json_format(file_store):
    return file_store.filename.endswith('json')


def is_xlsx_format(file_store):
    return file_store.filename.endswith('xlsx')


def get_ac(file_store):
    stream = file_store.stream
    if is_xlsx_format(file_store):
        stream.seek(0)
        return from_xlsx.build_full_ac(stream)
    elif is_json_format(file_store):
        stream.seek(0)
        json_data = json.load(stream)
        return build_full_ac_from_json(json_data)


def get_output_format(file_store):
    if is_json_format(file_store):
        return '.xlsx'
    elif is_xlsx_format(file_store):
        return '.json'


def get_output_file(ac, file_store):
    if is_json_format(file_store):
        wb = get_workbook(ac)
        return base64.b64encode(save_virtual_workbook(wb))
    elif is_xlsx_format(file_store):
        return ac.dump()


def build_error_response_message(e):
    stream = io.StringIO()
    stream.write("File is not a assay xlsx or assay json file: " + e.message + "\n")
    stream.write("\n\n")
    traceback.print_exc(file=stream)
    return '\n\n'.join(stream.getvalue().splitlines())


def get_filename(ac):
    return ac.name + "_" + datetime.datetime.now().strftime("%Y_%m_%d_T%H_%M_%S")


def is_valid_data(file_store):
    return is_valid_json_ac(file_store) or is_valid_xlsx_ac(file_store)