import arrow
import os

from flask import current_app
from openpyxl import Workbook


def load_data(filename):
    filename = os.path.join(current_app.config.get(''), filename)


def dump_data(data, filename=''):
    filename = filename if filename else '{}.xlsx'.format(arrow.now().format('YYYY-MM-DD'))
    directory = current_app.config.get('')
    file_name = os.path.join(directory, filename)
    wb = Workbook()
    ws = wb.create_sheet('数据', 0)
    headers = list(data[0].keys())
    ws.append(headers)
    for d in data:
        ws.append([d.get(key) for key in headers])
    wb.save(file_name)
    return directory, filename
