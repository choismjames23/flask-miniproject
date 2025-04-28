#from flask import Blueprint
from app.services.questions import questions_blp
from app.services.users import users_blp
from app.services.images import images_blp
from app.services.answers import answers_blp
from app.services.choices import choices_blp

# Flask app에서 Blueprint들을 등록할 때 사용할 blueprint 묶음
#api = Blueprint('api', __name__)

# 개별 Blueprint 등록
# api.register_blueprint(questions_blp)
# api.register_blueprint(users_blp)
# api.register_blueprint(images_blp)
# api.register_blueprint(answers_blp)
# api.register_blueprint(choices_blp)

# 여기는 Blueprint를 묶지 않고 개별 blueprint만 export
__all__ = [
    "questions_blp",
    "users_blp",
    "images_blp",
    "answers_blp",
    "choices_blp"
]