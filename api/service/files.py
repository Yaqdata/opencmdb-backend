from flask import send_from_directory
from webargs.flaskparser import use_args

from api.utils.custom.resource import BaseResource
from api.utils.custom.schema import download_schema
from api.utils.custom.files import dump_data
from api.models import (Instance, Mould)


class ExportResource(BaseResource):
    @use_args(download_schema)
    def post(self, args):
        mould_id = args.get('mould_id')
        mould = Mould.find_by_pk(mould_id)
        instances = Instance.fetch_all(mould=mould)
        filename = args.get('filename', '{}.xlsx')
        headers = mould.get_attributes_mapping()
        directory, filename = dump_data([i.abilities for i in instances], filename, headers)
        return send_from_directory(directory, filename, as_attachment=True)
