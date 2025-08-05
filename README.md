# Finday Face Verification Server

> Finday 프로젝트의 **얼굴 인증 전용 Flask API 서버**입니다.  
> 사용자의 웹캠으로 촬영된 실시간 이미지와, 등록된 얼굴 이미지(S3 저장)를  
> ArcFace 기반 DeepFace 모델로 비교하여 얼굴 인증 여부를 판단합니다.

---

## 프로젝트 역할

이 서버는 Finday의 **2단계 로그인 인증(얼굴 인증)** 기능을 처리합니다.  
1차 로그인(이메일/비밀번호) 후, **웹캠으로 촬영한 얼굴 이미지**와  
**등록된 얼굴 이미지(S3 URL)**를 비교하여 인증 결과를 반환합니다.

---

## 얼굴 인증 흐름

Finday 프론트엔드에서는 먼저 얼굴을 인식한 후 자동으로 캡처하고,  
해당 캡처 이미지를 이 Flask 서버에 전송하여 실제 유사도 비교를 수행합니다.

### 👁️‍🗨️ 얼굴 인증 흐름 요약

1. 사용자가 로그인 후 얼굴 인증 단계로 진입
2. 브라우저에서 `face-api.js`로 얼굴 감지 수행
3. 감지되면 3초 카운트 후 자동 캡처 (얼굴만 잘라냄)
4. Flask 서버에 캡처 이미지 + 등록 이미지(S3 URL) 전송
5. DeepFace(ArcFace)로 유사도 비교 수행
6. 인증 성공 여부(`success`, `distance`, `threshold`) 반환

---

## 얼굴 인증 시연 영상

아래 영상에서는 Finday의 **얼굴 인증 로그인 흐름**을 확인할 수 있습니다.

https://github.com/user-attachments/assets/99ca538e-69ec-457e-98d1-bcc9b9bfeec3

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;


## 기술 스택

| 항목 | 내용 |
|------|------|
| **백엔드 프레임워크** | Flask |
| **AI 모델** | DeepFace (`ArcFace` + `RetinaFace`) |
| **이미지 처리** | OpenCV, NumPy |
| **스토리지** | AWS S3 |
| **요청 전송** | requests, Flask `request.files` |
| **CORS** | flask-cors (모든 Origin 허용) |

---

## 프로젝트 구조

```
finday-face-verification/
├── app.py # Flask 메인 서버
├── config.py # AWS 키 등 민감 정보 분리 (git ignore)
├── config.py.example # 환경 설정 예시
├── requirements.txt # 의존성 목록
└── README.md # 프로젝트 설명
```

---

## API 명세

### [POST] `/verify-face`

웹캠 캡처 이미지와 S3에 등록된 사용자 이미지를 비교하여 얼굴 인증을 수행합니다.

**요청 형식:** `multipart/form-data`

| 필드 | 타입 | 설명 |
|------|------|------|
| `face_image` | file | 사용자의 캡처 이미지 |
| `face_img_url` | string | S3에 저장된 등록 이미지의 URL |

**성공 응답 (`200 OK`):**
```json
{
  "result": "success",
  "distance": 0.34,
  "threshold": 0.55
}
```
실패 응답 (401 Unauthorized):
```json
{
  "result": "fail",
  "reason": "NotMatched",
  "distance": 0.76,
  "threshold": 0.55
}
```
예외 응답 (500 Server Error):
```json
{
  "result": "fail",
  "reason": "Some error message"
}
```
## 환경 설정

### config.py 예시

```python
# config.py
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
BUCKET_NAME = 'finday-face-bucket'
```
✅ 해당 파일은 절대 커밋하지 마세요
→ 대신 config.py.example을 참고하여 직접 생성하세요.

.gitignore 설정
```gitignore
config.py
__pycache__/
*.pyc
.env
```

## 관련 레포지토리

| 서비스 | 레포지토리 |
|--------|-------------|
| 🌐 Finday 프론트엔드 | [`finday-frontend`](https://github.com/your-username/finday-frontend) |
| 🧠 Finday 백엔드 | [`finday-backend`](https://github.com/your-username/finday-backend) |
| 💳 국민은행 서버 | [`finday-bank-kb`](https://github.com/your-username/finday-bank-kb) |
| 💳 신한은행 서버 | [`finday-bank-shinhan`](https://github.com/your-username/finday-bank-shinhan) |
