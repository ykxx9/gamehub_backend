from app import app
from extensions import db
from sqlalchemy import inspect

# with app.app_context():
#     db.create_all()
    



with app.app_context():
    ins = inspect(db.engine)
    cl = ins.get_columns('Game')

    for i in cl:
        print(i['name'], i['type'])

