from flask import request, jsonify
from flask_smorest import Blueprint
from config import db
from app.models import Choices, datetime, KST, Question

choices_blp = Blueprint('Choices', 'choices', description='Operations on choices', url_prefix='/choices')

# 전체 선택지 조회
@choices_blp.route('/', methods=['GET'])
def get_choices():
    choices = Choices.query.all()
    return jsonify([c.to_dict() for c in choices])

# 선택지 추가
@choices_blp.route('/', methods=['POST'])
def add_choice():
    data = request.json
    new_choice = Choices(
        content=data['content'],
        is_active=data['is_active'],
        sqe=data['sqe'],
        question_id=data['question_id']
    )
    db.session.add(new_choice)
    db.session.commit()
    return jsonify({'message': f"Content: '{new_choice.content}' choice Success Create"}), 201

# 특정 질문에 대한 선택지 조회
@choices_blp.route('/<int:question_id>', methods=['GET'])
def get_choice(question_id):
    choices = Choices.query.filter_by(question_id=question_id).all()
    return jsonify({
        "choices": [
            {"id": choice.id, "content": choice.content, "is_active": choice.is_active}
                for choice in choices
        ]
    })

# 선택지 수정
@choices_blp.route('/<int:choice_id>', methods=['PUT'])
def update_choice(choice_id):
    choice = Choices.query.get_or_404(choice_id)
    data = request.json
    choice.content = data.get('content', choice.content)
    choice.is_active = data.get('is_active', choice.is_active)
    choice.sqe = data.get('sqe', choice.sqe)
    choice.updated_at = datetime.now(tz=KST)
    db.session.commit()
    return jsonify({'msg': 'Updated Choice', 'choice': choice.to_dict()}), 200

# 선택지 삭제
@choices_blp.route('/<int:choice_id>', methods=['DELETE'])
def delete_choice(choice_id):
    choice = Choices.query.get_or_404(choice_id)
    db.session.delete(choice)
    db.session.commit()
    return jsonify({'msg': 'Deleted Choice'})