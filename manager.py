from flask_script import Manager

from api import create_app

manager = Manager(create_app)


@manager.command
def init_user_info():
    from scripts.init_user_info import init_user_info
    init_user_info()


if __name__ == '__main__':
    manager.run()
