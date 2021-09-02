from flask import jsonify, json, make_response

from app.models import DBModel
from app import db


def add_user_to_db(input_user: dict) -> None:
    """Добавление пользоватя в базу данных"""
    user = DBModel.User(
        name=input_user['name'],
        surname=input_user['surname'],
        email=input_user['email'],
        image=input_user['image']
    )
    user.set_password(input_user['password'])
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as error:
        return return_error(error)
    return


def remove_user_from_db(data_input: json) -> json:
    """Удаление пользователя из базы данных"""
    try:
        u = DBModel.Task.query.filter_by(id=data_input['id']).first()
    except Exception as error:
        return return_error(error)
    db.session.delete(u)
    return return_ok()


def user_authorization(user_username: str, user_email: str, user_password: str) -> json:
    """Авторизует пользователя в системе"""

    def user_identification(username: str, email: str, password: str) -> bool:
        """Проверяет наличия пользователя в базе"""
        try:
            checking_availability = DBModel.User.query.filter_by(name=username).scalar()
        except Exception as error:
            return return_error(error)
        if checking_availability is not None:
            return user_authentication(username, email, password)
        else:
            return make_response(jsonify(
                {
                    'response': 'error',
                    'error': 'There is no such user'
                }
            ))

    def user_authentication(username: str, email: str, password: str) -> bool:
        """Проверяет соответсвия данных пользователя"""
        try:
            u = DBModel.User.query.filter_by(name=username).first()
        except Exception as error:
            return return_error(error)
        if (username == u.name) and (email == u.email) and u.check_password(password):
            return u.serialize

    user = user_identification(user_username, user_email, user_password)
    return user


def add_task(data_input: json) -> json:
    """Добавление задачи"""
    task = DBModel.Task(
        body=data_input['body'],
        description=data_input['description'],
        user_id=data_input['user_id'],
        done=data_input['done'],
        file=data_input['file']
    )
    db.session.add(task)
    db.session.commit()
    return return_ok()


def drop_task(data_input: json) -> json:
    """Удаление задачи"""
    try:
        t = DBModel.Task.query.filter_by(id=data_input['id']).first()
    except Exception as error:
        return return_error(error)
    db.session.delete(t)
    return return_ok()


def show_task(data_input: json) -> json:
    """Визуализация задачи"""
    try:
        tasks = DBModel.Task.query.filter_by(user_id=data_input['user_id']).all()
    except Exception as error:
        return return_error(error)
    tasks = [x.serialize for x in tasks]
    print(tasks)
    return jsonify({'task': tasks})


def update_task(data_input: json) -> json:
    """Обновление задачи"""
    try:
        task = DBModel.Task.query.filter_by(user_id=data_input['user_id'],
                                            id=data_input['task_id'])
    except Exception as error:
        return return_error(error)
    task.body = data_input['body']
    task.description = data_input['description']
    task.done = data_input['done']
    task.file = data_input['file']
    db.session.update(task)
    db.session.commit()
    return return_ok()


def return_error(error) -> json:
    """Возвращает ошибку"""
    print(error)
    return make_response(jsonify(
        {
            'response': 'error again',
            'error': str(error)
        }
    ))


def return_ok() -> json:
    """Возвращает удачный """
    return jsonify({'response': 'OK'}), 201
