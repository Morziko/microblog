'''
Created on 13 січ. 2019 р.

@author: YURA
'''
from app import create_app, db, cli
from app.models import *


app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notification, 'Preambul': Preambul, 'Test':Test,
            'HistoryCurrency': HistoryCurrency, 'HistoryCity': HistoryCity,
            'Currency': Currency, 'City': City, 'FileContent': FileContent}

if __name__ == '__main__':
    app.run(debug=True)
