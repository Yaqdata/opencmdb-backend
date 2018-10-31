from webargs.flaskparser import use_args

from api.utils.custom.resource import BaseResource
from api.utils.custom.schema import user_schema
from api.models import User
from api.utils.custom.error import error
from api.utils.custom.interface_tips import InterfaceTips


class LoginResource(BaseResource):
    @use_args(user_schema)
    def post(self, args):
        user = User.get_user_by_email(args.get('email'))
        if not user:
            error(InterfaceTips.USER_NOT_EXISTED_OR_WRONG_PASSWORD)

        if not user.verify_password(args.get('password')):
            error(InterfaceTips.USER_NOT_EXISTED_OR_WRONG_PASSWORD)

        user_data = user_schema.dump(user).data
        user_data.update({'authentication_token': user.get_auth_token()})

        return user_data