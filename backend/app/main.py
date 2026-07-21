import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.generate import router as generate_router

# 1. إنشاء تطبيق FastAPI
app = FastAPI(
    title="3D AI Generation Engine",
    version="1.0.0"
)

# 2. إعدادات الـ CORS للسماح بالاتصال من أي عنوان (بما فيها IP الشبكة المحلية)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. تحديد المسار المطلق لمجلد المخرجات وإنشائه تلقائياً إذا لم يكن موجوداً
base_dir = os.path.dirname(os.path.abspath(__file__))  # backend/app
outputs_path = os.path.join(base_dir, "outputs")      # backend/app/outputs
os.makedirs(outputs_path, exist_ok=True)

# 4. ربط مجلد المخرجات لتقديم ملفات الـ GLB مباشرة عبر المسار /outputs
app.mount("/outputs", StaticFiles(directory=outputs_path), name="outputs")

# 5. تضمين الـ Router الخاص بتوليد المجسمات
app.include_router(generate_router)


# 6. نقطة النهاية الأساسية للتحقق من حالة السيرفر
@app.get("/")
def read_root():
    return {"status": "AI Engine is running smoothly"}