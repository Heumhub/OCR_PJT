# FastAPI OCR 시스템

## 📖 소개
FastAPI 기반으로 만든 OCR(Optical Character Recognition) 시스템입니다.  
Tesseract OCR을 활용하여 이미지에서 텍스트를 추출하고, AWS Lambda에 배포할 수 있도록 설계되었습니다.

## 🚀 기능
- 이미지에서 텍스트 추출 (Tesseract OCR)
- 특정 정보(예: 이름, 날짜, 주소 등)의 좌표 반환
- 자동 Blur 처리 기능
- FastAPI + Uvicorn 서버
- AWS Lambda 배포 가능

## 🛠️ 설치 방법
### 1️⃣ 필수 패키지 설치
```bash
pip install -r requirements.txt

Tesseract OCR 설치 (필요한 경우)
https://github.com/ub-mannheim/tesseract/wiki
