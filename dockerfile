# 베이스 이미지
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요 파일 복사
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 포트 노출 (예: 8000)
EXPOSE 8000

# 실행 커맨드 (예: uvicorn main:app --host 0.0.0.0 --port 8000)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
