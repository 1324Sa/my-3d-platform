import os
import sys
import uuid
import torch
from PIL import Image

# 1. البحث عن مجلد TripoSR وإضافته إلى مسارات النظام تلقائياً
current_dir = os.path.dirname(os.path.abspath(__file__))  # backend/app/services
app_dir = os.path.dirname(current_dir)                  # backend/app
backend_dir = os.path.dirname(app_dir)                  # backend
project_root = os.path.dirname(backend_dir)             # my-3d-platform

# التحقق من مسارات TripoSR الممكنة
possible_paths = [
    os.path.join(project_root, "TripoSR"),               # my-3d-platform/TripoSR
    os.path.join(backend_dir, "TripoSR"),                # backend/TripoSR
]

for path in possible_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)
        break

# 2. استيراد مكونات TripoSR
try:
    from tsr.system import TSR
except ModuleNotFoundError as e:
    raise RuntimeError(
        f"لم يتم العثور على مجلد tsr! تأكد من وجود مجلد TripoSR داخل المشروع. الخطأ التفصيلي: {e}"
    )

# 3. تهيئة النموذج وتحديد وحدة المعالجة (GPU / CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = TSR.from_pretrained(
    "stabilityai/TripoSR",
    config_name="config.yaml",
    weight_name="model.ckpt",
)
model.renderer.set_chunk_size(131072)
model.to(device)


def generate_3d_model_from_pil(image: Image.Image) -> str:
    """
    تستقبل الصورة المعالجة، تولد مجسم 3D بـ TripoSR، 
    وتحفظ ملف الـ GLB في مجلد outputs وتُرجع مساره المطلق.
    """
    # تحديد مسار مجلد المخرجات (backend/app/outputs)
    outputs_dir = os.path.join(app_dir, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)

    # تمرير الصورة داخل قائمة [image] للنموذج
    with torch.no_grad():
        scene_codes = model([image], device=device)

    # استخراج الـ Mesh من التوليد
    meshes = model.extract_mesh(scene_codes, True)[0]

    # إنشاء اسم فريد وتصدير ملف GLB النهائي
    filename = f"model_{uuid.uuid4().hex[:8]}.glb"
    output_path = os.path.join(outputs_dir, filename)
    meshes.export(output_path)

    print(f"✅ تم حفظ الملف بنجاح في: {output_path}")
    return output_path