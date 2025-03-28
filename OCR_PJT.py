import pytesseract
from PIL import Image
import re
import os

# Tesseract 실행 파일 경로 설정 (Windows 기준)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 검사할 이미지가 들어 있는 폴더 경로
image_folder = "./image"  # 검사할 이미지 폴더

# 정규 표현식 패턴들
patterns = {
    "이메일 주소 (Email address)": r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
    "이름 (Names)": r'[가-힣]{2,4}\s?[가-힣]{1,4}',
    "전화번호 (Phone numbers)": r'(?:010|011|016|017|018|019)-\d{3,4}-\d{4}|\b0\d{1,2}-\d{3,4}-\d{4}\b',
    "주민등록번호 (RRN)": r'\b\d{6}-\d{7}\b',
    "고유 식별자 (Unique ID)": r'\b(?:USR|EMP)-\d{4,6}\b',
    "신용카드 번호 (Credit Card)": r'\b(?:\d{4}[- ]?){3}\d{4}\b',
    "계좌번호 (Bank Account)": r'\b\d{2,3}-\d{3,4}-\d{4,6}\b',
    "금액 정보 (Money)": r'\₩?\d{1,3}(?:,\d{3})*(?:\.\d+)?',
    "사업자등록번호 (Business Reg)": r'\b\d{3}-\d{2}-\d{5}\b',
    "세금 관련 번호 (Taxpayer)": r'\b\d{3}-\d{2}-\d{6,10}\b',
    "웹사이트 주소 (URLs)": r'https?://[a-zA-Z0-9./?=&_-]+',
    "IP 주소 (IP Address)": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    "MAC 주소 (MAC Address)": r'\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b',
    "차량 번호판 (License Plate)": r'\b[가-힣]{1,2}\s?\d{1,4}\s?[가-힣]\s?\d{4}\b',
    "커스텀 필터 (Custom)": r'\b(?:내부문서-\d{4}|보안등급:\s?[가-힣]+)\b'
}

# 폴더 내 모든 이미지 파일 찾기
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
print(image_files)
if not image_files:
    print(f"오류: '{image_folder}' 폴더에 이미지가 없습니다!")
    exit()

# 모든 이미지 파일에 대해 OCR 실행
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    img = Image.open(image_path)

    # OCR을 통해 이미지에서 텍스트 및 좌표 추출
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    # 탐지된 개인정보 저장 리스트
    found_results = []

    # 텍스트 데이터에서 모든 단어 검사
    for i, word in enumerate(data['text']):
        for label, pattern in patterns.items():
            if re.search(pattern, word):  # 정규식 패턴에 해당하면 저장
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                found_results.append({
                    "label": label,
                    "text": word,
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h
                })
# x: 텍스트 영역의 왼쪽 상단 모서리의 X 좌표
# y: 텍스트 영역의 왼쪽 상단 모서리의 Y 좌표
# w (width): 텍스트 영역의 너비
# h (height): 텍스트 영역의 높이 ((x, y)는 글자가 시작하는 위치이며 w와 h는 해당 글자의 크기를 나타냄)


# 결과 출력
print(f"\n [파일] {image_file}")
if found_results:
    for result in found_results:
        print(f"[{result['label']}] {result['text']} → 좌표: (x={result['x']}, y={result['y']}, w={result['width']}, h={result['height']})")
else:
    print("일치하는 정보가 없습니다.")

