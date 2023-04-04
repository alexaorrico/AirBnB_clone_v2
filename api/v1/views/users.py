#!/usr/bin/python3
"""User flask file for holberton API"""
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from api.v1.models import User, db

users_bp = Blueprint('users', __name__)


@users_bp.route('/api/v1/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@users_bp.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@users_bp.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({}), 200


@users_bp.route('/api/v1/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in data:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in data:
        return jsonify({'error': 'Missing password'}), 400

    try:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 400

    return jsonify(user.to_dict()), 201


@users_bp.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    for key, value in data.items():
        if key not in ('id', 'email', 'created_at', 'updated_at'):
            setattr(user, key, value)

    db.session.commit()
    return jsonify(user.to_dict()), 200
