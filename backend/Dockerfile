FROM python:3.10-slim

# تثبيت الحزم الأساسية للنظام
RUN apt-get update && apt-get install -y \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# نسخ وتثبيت الاعتمادات
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /code/requirements.txt

# نسخ كود المشروع
COPY . /code

# إعطاء صلاحيات للمجلدات
RUN chmod -R 777 /code

# تشغيل FastAPI على المنفذ 7860 (المنفذ الافتراضي لـ Hugging Face)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]