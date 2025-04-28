from flask import request, jsonify
from flask_smorest import Blueprint
from config import db
from app.models import User, datetime, KST

users_blp = Blueprint('Users', 'users', description='Operations on users', url_prefix='/users')

# 전체 사용자 조회
@users_blp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# 특정 사용자 조회
@users_blp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# 특정 사용자 수정
@users_blp.route('/<int:user_id>', methods=['PUT'])
def put_user(user_id: int):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.name = data.get('name', user.name)
    user.age = data.get('age', user.age)
    user.gender = data.get('gender', user.gender)
    user.email = data.get('email', user.email)
    user.updated_at = datetime.now(tz=KST)  # 현재 시간으로 업데이트
    db.session.commit()
    return jsonify({'msg': 'Updated User', 'user': user.to_dict()}), 201

# 특정 사용자 삭제
@users_blp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'Deleted User'})