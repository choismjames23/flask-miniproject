from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_smorest import Api
from app.routes import questions_blp, users_blp, images_blp, answers_blp, choices_blp
from config import db
from app.models import Answer, User

migrate = Migrate()


def create_app():
    #앱 설정
    application = Flask(__name__)

    #초기값 설정
    application.config.from_object("config.Config")
    application.secret_key = "oz_form_secret"

    #db 설정
    db.init_app(application)
    migrate.init_app(application, db)

    api = Api(application)

    #초기 화면
    @application.route('/', methods=['GET'])
    def default():
        return jsonify({"message": "Success Connect"})
    
		# 400 에러 발생 시, JSON 형태로 응답 반환
    @application.errorhandler(400)
    def handle_bad_request(error):
        response = jsonify({"message": error.description})
        response.status_code = 400
        return response
    
    #회원 가입
    @application.route('/signup', methods=['POST'])
    def post_user():
        data = request.json
        new_user = User(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            email=data['email']
        )

        if User.query.filter_by(email=new_user.email).first():
            return jsonify({"message": "이미 존재하는 계정입니다."}), 400
        
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': f'{new_user.name}님 회원가입을 축하합니다',
                        'user_id': new_user.id}), 201
    
    #응답 제출
    @application.route('/submit', methods=['POST'])
    def submit():
        data = request.json

        for item in data:
            user_id = item.get("user_id")
            choice_id = item.get("choice_id")

            new_answer = Answer(user_id=user_id, choice_id=choice_id)
            db.session.add(new_answer)
        db.session.commit()

        return jsonify({
            'message': f"User {user_id}'s answers Success Create"
        })    

		# 플라스크 앱에 블루프린트 등록
    #application.register_blueprint(api, url_prefix='/api')

    #smorest 방식으로 api 블루프린트들을 등록
    api.register_blueprint(questions_blp)
    api.register_blueprint(users_blp)
    api.register_blueprint(images_blp)
    api.register_blueprint(answers_blp)
    api.register_blueprint(choices_blp)

    return application