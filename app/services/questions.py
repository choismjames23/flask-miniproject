from flask import request, jsonify
from flask_smorest import Blueprint
from config import db
from app.models import Question, datetime, KST , Choices, Image

questions_blp = Blueprint('Questions', 'questions', description='Operations on questions', url_prefix='/questions')

# 전체 질문 조회
@questions_blp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    return jsonify([q.to_dict() for q in questions])

# 질문 추가
@questions_blp.route('/', methods=['POST'])
def add_question():
    data = request.json
    new_question = Question(
        title=data['title'],
        is_active=data['is_active'],
        sqe=data['sqe'],
        image_id=data['image_id']
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({'message': f"Title: '{new_question.title}' question Success Create"}), 201

# 질문 개수 확인
@questions_blp.route('/count', methods=['GET'])
def count_question():
    count = Question.query.count()
    return jsonify({"total": count})

# 개별 질문 조회
@questions_blp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.get_or_404(question_id)
    choices = Choices.query.filter_by(question_id = question_id).all()
    image_url = question.image.url if question.image else None
    return jsonify({
        "id": question.id,
        "title": question.title,
        "image": image_url,
        "choices": [
            {"id": choice.id, "content": choice.content, "is_active": choice.is_active}
                for choice in choices
        ]
        })

# 질문 수정
@questions_blp.route('/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.json
    question.title = data.get('title', question.title)
    question.is_active = data.get('is_active', question.is_active)
    question.sqe = data.get('sqe', question.sqe)
    question.updated_at = datetime.now(tz=KST)
    db.session.commit()
    return jsonify({'msg': 'Updated Question', 'question': question.to_dict()}), 200

# 질문 삭제
@questions_blp.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'msg': 'Deleted Question'})