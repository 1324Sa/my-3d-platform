import io
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from rembg import remove
from PIL import Image

# استيراد دالة التوليد الخاصة بنموذج TripoSR
from app.services.triposr import generate_3d_model_from_pil 

router = APIRouter(prefix="/api/v1", tags=["3D Generation"])


@router.post("/generate-from-image")
async def generate_from_image(file: UploadFile = File(...)):
    try:
        # 1. قراءة بيانات الصورة المرسلة
        input_image_bytes = await file.read()

        # 2. تفريغ خلفية الصورة تلقائياً باستخدام rembg
        output_image_bytes = remove(input_image_bytes)
        processed_image = Image.open(io.BytesIO(output_image_bytes)).convert("RGBA")

        # 3. معالجة القناة الشفافة لتحويل الصورة إلى RGB بخلفية بيضاء بدلاً من RGBA
        background = Image.new("RGBA", processed_image.size, (255, 255, 255))
        alpha_composite = Image.alpha_composite(background, processed_image)
        rgb_image = alpha_composite.convert("RGB")

        # 4. تمرير الصورة المعالجة (RGB) لنموذج TripoSR لتوليد الـ GLB
        output_glb_path = generate_3d_model_from_pil(rgb_image)

        # 5. إرجاع المسار النسبي للملف المولد
        filename = os.path.basename(output_glb_path)
        return {"model_url": f"/outputs/{filename}"}

    except Exception as e:
        print(f"Error during generation: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"حدث خطأ أثناء تفريغ الخلفية وتوليد المجسم: {str(e)}"
        )