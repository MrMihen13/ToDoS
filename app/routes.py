import json

from flask import request, jsonify, make_response
from pydantic import ValidationError

from app import app
from app.models import ValidationModel
from app.logic import (add_user_to_db, user_authorization,
                       add_task, drop_task, update_task, show_task)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def get_tasks():
    """Тестовая функция, можно удалить"""
    try:
        return "OK"
    except Exception as error:
        return return_error(error)


@app.route('/todos/v1.0/login/', methods=['GET'])
def login() -> json:
    """Проверяет данные пользователя на соответсвие в бозе.
    Возвращает данные пользователя или ошибку"""
    try:
        valid_user = ValidationModel.InputUser.parse_raw(request.get_json())
    except ValidationError:
        return return_validation_error()
    user = user_authorization(valid_user.name, valid_user.email, valid_user.password)
    return jsonify({'user': user})


@app.route('/todo/v1.0/registration/')
def registration() -> json:
    """Регистрирует пользователя в ситеме.
    Возвращиет данные пользователя или ошибку"""
    try:
        valid_user = ValidationModel.InputUser.parse_raw(request.get_json())
    except ValidationError:
        return return_validation_error()
    add_user_to_db(valid_user.__dict__)
    return return_ok()


@app.route('/todos/v1.0/tasks', methods=['POST', 'GET', 'PUT', 'DELETE'])
def todo():
    """Обрабатывает логику работы с задачами"""
    process_methods = {
        'POST': add_task,
        'GET': show_task,
        'PUT': update_task,
        'DELETE': drop_task
    }
    try:
        valid_task = ValidationModel.InputTask.parse_raw(request.get_json())
    except ValidationError:
        return return_validation_error()
    process_methods[request.method](valid_task.__dict__)


@app.errorhandler(404)
def not_found(error) -> json:
    """Возвращает ошибку Not fount 404"""
    print(error)
    return make_response(jsonify({'error': 'Not found'}), 404)


def return_ok() -> json:
    """Возвращает удачный """
    return jsonify({'response': 'OK'}), 201


def return_error(error) -> json:
    """Возвращает ошибку"""
    print(error)
    return make_response(jsonify(
        {
            'response': 'error again',
            'error': str(error)
        }
    ))


def return_validation_error() -> json:
    """Возвращает ошибку валидации"""
    return make_response(jsonify(
        {
            'response': 'error',
            'error': 'Incorrect data was entered'
        }
    ))
