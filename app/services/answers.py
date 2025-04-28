from flask import request, jsonify
from flask_smorest import Blueprint
from config import db
from app.models import Answer, datetime, KST

answers_blp = Blueprint('Answers', 'answers', description='Operations on answers', url_prefix='/answers')

# 전체 답변 조회
@answers_blp.route('/', methods=['GET'])
def get_answers():
    answers = Answer.query.all()
    return jsonify([a.to_dict() for a in answers])

# 답변 제출
@answers_blp.route('/', methods=['POST'])
def submit_answer():
    data = request.json
    new_answer = Answer(
        question_id=data['question_id'],
        choice_id=data['choice_id']
    )
    db.session.add(new_answer)
    db.session.commit()
    return jsonify({'msg': 'Submitted Answer'}), 201

# 개별 답변 조회
@answers_blp.route('/<int:answer_id>', methods=['GET'])
def get_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    return jsonify(answer.to_dict())

# 답변 삭제
@answers_blp.route('/<int:answer_id>', methods=['DELETE'])
def delete_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    db.session.delete(answer)
    db.session.commit()
    return jsonify({'msg': 'Deleted Answer'})