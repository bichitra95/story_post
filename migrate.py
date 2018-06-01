from flask_migrate import MigrateCommand , Migrate
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from apis import create_app
from apis.models import db

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()