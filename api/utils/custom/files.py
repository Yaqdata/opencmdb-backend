import arrow
import os

from flask import current_app
from openpyxl import Workbook


def dump_data(data, headers, filename=''):
    filename = filename if filename else '{}.xlsx'.format(arrow.now().format('YYYY-MM-DD'))
    directory = current_app.config.get('FILE_DIRECTORY')
    file_name = os.path.join(directory, filename)
    wb = Workbook()
    ws = wb.create_sheet('数据', 0)
    ws.append([head.get('attribute_name') for head in headers])
    for d in data:
        ws.append([d.get(header.get('attribute_code')) for header in headers])
    wb.save(file_name)
    return directory, filename
