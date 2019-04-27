from api.utils.custom.resource import BaseResource


class DemoResource(BaseResource):
    @BaseResource.request_log('demo')
    def get(self):
        return {'test': 'test'}
