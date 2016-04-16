from io import StringIO
from dwarfsquad.lib.build import from_xlsx, from_json
from dwarfsquad.lib.build.from_json.helpers import build_full_ac_from_json
from dwarfsquad.lib.export.export_full_ac import get_workbook
from flask import Response, stream_with_context, make_response
import json
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook


def is_xlsx(file_store):
    try:
        assert file_store.filename.endswith('xlsx')
        wb = load_workbook(file_store.stream)
        from_xlsx.validate_workbook(wb)
        return True
    except:
        return False


def is_json(file_store):
    try:
        assert file_store.filename.endswith('json')
        json_data = json.load(file_store.stream)
        from_json.validate_json(json_data)
        return True
    except:
        return False


def convert_data(request):
    for file_store in request.files.values():
        if is_xlsx(file_store):
            ac = from_xlsx.build_full_ac(file_store.stream)
            resp = make_response(ac.dump(), 200)
            resp.headers['Content-Disposition'] = "attachment; filename=test.json"
            return resp
        elif is_json(file_store):
            file_store.stream.seek(0)
            json_data = json.load(file_store.stream)
            ac = build_full_ac_from_json(json_data)
            wb = get_workbook(ac)
            resp = Response(stream_with_context(save_virtual_workbook(wb)), 200)
            resp.headers['Content-Disposition'] = "attachment; filename=text.xlsx"
            return resp
