from flask import Flask, request, jsonify
import cv2
import numpy as np
import boto3
from deepface import DeepFace
import traceback
import requests
from flask_cors import CORS
import config  # ← 추가


app = Flask(__name__)
CORS(app)  # 이 줄 추가하면 모든 Origin 허용

# S3 설정
s3 = boto3.client(
    's3',
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
)
BUCKET_NAME = config.BUCKET_NAME

@app.route('/verify-face', methods=['POST'])
def verify_face():
    try:
        # 1. 전달받은 이미지 (웹캡 캡처본)와 사용자 등록 이미지(S3 주소)를 읽는다
        face_img_file = request.files['face_image']
        registered_img_url = request.form.get('face_img_url')  # S3 등록 이미지 URL

        # 2. 캡처 이미지 → OpenCV 이미지
        uploaded_bytes = face_img_file.read()
        webcam_img = cv2.imdecode(np.frombuffer(uploaded_bytes, np.uint8), cv2.IMREAD_COLOR)

        # 3. 등록 이미지 다운로드
        if not registered_img_url.startswith('https://'):
            return jsonify({'result': 'fail', 'reason': 'InvalidImageURL'}), 400

        s3_bytes = requests.get(registered_img_url).content
        s3_img = cv2.imdecode(np.frombuffer(s3_bytes, np.uint8), cv2.IMREAD_COLOR)

        # 4. 얼굴 검증 수행 (ArcFace + retinaface)
        result = DeepFace.verify(
            img1_path=webcam_img,
            img2_path=s3_img,
            detector_backend='retinaface',
            model_name='ArcFace',
            enforce_detection=False
        )

        if result['verified']:
            return jsonify({
                'result': 'success',
                'distance': result['distance'],
                'threshold': result['threshold']
            }), 200
        else:
            return jsonify({
                'result': 'fail',
                'reason': 'NotMatched',
                'distance': result['distance'],
                'threshold': result['threshold']
            }), 401

    except Exception as e:
        traceback.print_exc()
        return jsonify({'result': 'fail', 'reason': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
