from flask import request, jsonify
from flask_smorest import Blueprint
from config import db
from app.models import Image, datetime, KST

images_blp = Blueprint('Images', 'images', description='Operations on images', url_prefix='/images')

# 전체 이미지 조회
@images_blp.route('/', methods=['GET'])
def get_images():
    images = Image.query.all()
    return jsonify([image.to_dict() for image in images])

# 이미지 추가
@images_blp.route('/', methods=['POST'])
def add_image():
    data = request.json
    new_image = Image(
        url=data['url'],
        image_type=data['type']
    )
    db.session.add(new_image)
    db.session.commit()
    return jsonify({'message': f"ID: {new_image.id} Image Success Create"}), 201

# 개별 이미지 조회
@images_blp.route('/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = Image.query.get_or_404(image_id)
    return jsonify(image.to_dict())

# 메인 이미지 조회
@images_blp.route('/main', methods=['GET'])
def get_main_image():
    images = Image.query.filter_by(type="main").all()
    return jsonify({"main image": [f"image_id: {image.id}, url: {image.url}" for image in images]})

# 이미지 수정
@images_blp.route('/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    image = Image.query.get_or_404(image_id)
    data = request.json
    image.url = data.get('url', image.url)
    image.type = data.get('type', image.type)
    image.updated_at = datetime.now(tz=KST)
    db.session.commit()
    return jsonify({'msg': 'Updated Image', 'image': image.to_dict()}), 200

# 이미지 삭제
@images_blp.route('/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    return jsonify({'msg': 'Deleted Image'})