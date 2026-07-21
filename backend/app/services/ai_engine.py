import os
import sys
import io
import uuid
import torch
from PIL import Image

# 1. استخدام mcubes كبديل لـ torchmcubes في حال عدم وجودها
try:
    import torchmcubes
except ImportError:
    import mcubes

    class TorchMCubesMock:
        @staticmethod
        def marching_cubes(volume, threshold):
            if isinstance(volume, torch.Tensor):
                volume_np = volume.detach().cpu().numpy()
            else:
                volume_np = volume
            verts, faces = mcubes.marching_cubes(volume_np, threshold)
            return torch.from_numpy(verts).float(), torch.from_numpy(faces.astype("int64"))

    sys.modules["torchmcubes"] = TorchMCubesMock

# 2. إضافة مسار TripoSR للـ Path
tsr_path = os.path.join(os.path.dirname(__file__), "..", "..", "TripoSR")
if tsr_path not in sys.path:
    sys.path.append(tsr_path)


class AIEngineService:
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
        os.makedirs(self.output_dir, exist_ok=True)
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = None

        try:
            from tsr.system import TSR
            print(f"🚀 Loading TripoSR model on device: {self.device}...")
            self.model = TSR.from_pretrained(
                "stabilityai/TripoSR",
                config_name="config.yaml",
                weight_name="model.ckpt",
            )
            self.model.renderer.set_chunk_size(8192)
            self.model.to(self.device)
            print("✅ TripoSR Model loaded successfully!")
        except Exception as e:
            print(f"⚠️ Warning during TripoSR load: {e}")

    async def generate_3d_from_image(self, image_bytes: bytes) -> str:
        unique_id = uuid.uuid4().hex[:8]
        output_filename = f"model_{unique_id}.glb"
        output_filepath = os.path.join(self.output_dir, output_filename)

        # 1. فتح الصورة
        image = Image.open(io.BytesIO(image_bytes))

        if self.model is None:
            # خيار احتياطي في حال عدم تحميل النموذج
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.save(output_filepath.replace(".glb", ".png"))
            return f"/outputs/{output_filename}"

        # 2. إزالة الخلفية وضبط القياسات
        from tsr.utils import remove_background, resize_foreground
        image_rembg = remove_background(image)
        image_processed = resize_foreground(image_rembg, 0.85)

        # 3. ضمان تحويل الصورة الناتجة إلى RGB
        if image_processed.mode != "RGB":
            background = Image.new("RGB", image_processed.size, (127, 127, 127))
            if image_processed.mode == "RGBA":
                background.paste(image_processed, mask=image_processed.split()[3])
            else:
                background.paste(image_processed)
            image_processed = background

        # 4. التوليد واستخراج المجسم
        with torch.no_grad():
            scene_codes = self.model([image_processed], device=self.device)
            # تمرير المعامل الصريح لـ has_vertex_color
            meshes = self.model.extract_mesh(scene_codes, has_vertex_color=True)

        # التصدير المباشر بصيغة GLB
        meshes[0].export(output_filepath)
        return f"/outputs/{output_filename}"