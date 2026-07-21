import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from gradio_client import Client, handle_file

from app.api.generate import router as generate_router

# 1. إنشاء تطبيق FastAPI
app = FastAPI(
    title="3D AI Generation Engine",
    version="1.0.0"
)

# 2. إعدادات الـ CORS للسماح بالاتصال من الواجهات المختلفة
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. إعداد مجلد المخرجات المحلي (إن وجد)
base_dir = os.path.dirname(os.path.abspath(__file__))  # backend/app
outputs_path = os.path.join(base_dir, "outputs")       # backend/app/outputs
os.makedirs(outputs_path, exist_ok=True)

# 4. ربط مجلد المخرجات لتقديم الملفات عبر /outputs
app.mount("/outputs", StaticFiles(directory=outputs_path), name="outputs")

# 5. تضمين الـ Routers الخاصة بالمشروع
app.include_router(generate_router)

# 6. إعداد اسم الـ Space الخاص بـ Hugging Face
HF_SPACE_ID = "professsor7/my-3d-engine"


# 7. نقطة النهاية الأساسية للتحقق من حالة السيرفر
@app.get("/")
def read_root():
    return {"status": "AI Engine is running smoothly"}


# 8. Endpoint توليد الـ 3D عبر Hugging Face
@app.post("/generate-3d")
async def generate_3d_endpoint(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    
    # حفظ الصورة بشكل مؤقت
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # إرسال الصورة إلى Hugging Face للبدء في المعالجة
        client = Client(HF_SPACE_ID)
        result = client.predict(
            input_image=handle_file(temp_path),
            api_name="/predict"
        )
        return {"status": "success", "result": result}
        
    finally:
        # تنظيف وتحذيف الملف المؤقت من السيرفر
        if os.path.exists(temp_path):
            os.remove(temp_path)