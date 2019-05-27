from flask import Blueprint
from flask_restful import Api

from api.service.aggregation import (AggregationResource, AggregationsResource)
from api.service.demo import DemoResource
from api.service.login import LoginResource
from api.service.mould import (
    MouldResource, MouldsResource, AggregationMouldsResource, MouldTreeResource, MouldParentResource,
    MouldChildrenResource,
)
from api.service.instance import (
    InstancesResource, InstanceResource, InstanceTreeResource, InstanceParentResource,
    InstanceChildrenResource, BridgesInstancesResource, MouldInstanceStatsResource,
    CrawlInstances,
)
from api.service.operation_log import OperationLogsResource
from api.service.files import ExportResource

api_bp_v1 = Blueprint('bp_v0.1', __name__)
api_v1 = Api(api_bp_v1, '/api/v0.1')

api_v1.add_resource(DemoResource, '/demo')
api_v1.add_resource(LoginResource, '/login')
api_v1.add_resource(AggregationsResource, '/layers/<layer_id>/aggregations')
api_v1.add_resource(AggregationResource, '/aggregations/<aggregation_id>')
api_v1.add_resource(MouldsResource, '/moulds')
api_v1.add_resource(MouldResource, '/moulds/<mould_id>')
api_v1.add_resource(MouldTreeResource, '/layers/<layer_id>/moulds/tree')
api_v1.add_resource(MouldChildrenResource, '/moulds/<mould_id>/children')
api_v1.add_resource(MouldParentResource, '/moulds/<mould_id>/parent')
api_v1.add_resource(AggregationMouldsResource, '/layers/<layer_id>/aggregations/<aggregation_id>/moulds')
api_v1.add_resource(InstancesResource, '/moulds/<mould_id>/instances')
api_v1.add_resource(InstanceResource, '/instances/<instance_id>')
api_v1.add_resource(InstanceTreeResource, '/layers/<layer_id>/instances/tree')
api_v1.add_resource(InstanceParentResource, '/instances/<instance_id>/parent')
api_v1.add_resource(InstanceChildrenResource, '/instances/<instance_id>/children')
api_v1.add_resource(BridgesInstancesResource, '/bridges/instances')
api_v1.add_resource(MouldInstanceStatsResource, '/mould/instances/stats')
api_v1.add_resource(OperationLogsResource, '/operation/logs')
api_v1.add_resource(CrawlInstances, '/crawl/instances')
api_v1.add_resource(ExportResource, '/export')

BLUEPRINTS = [api_bp_v1]

__all__ = ['BLUEPRINTS']

