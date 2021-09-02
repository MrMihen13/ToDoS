from app import app, db
from app.models import DBModel


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': DBModel.User, 'Task': DBModel.Task}


if __name__ == "__main__":
    app.run(debug=True)
