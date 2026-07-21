"use client";

import React, { useState, useRef } from "react";
import ModelViewer from "@/components/ModelViewer";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [modelUrl, setModelUrl] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  // 1️⃣ معالجة اختيار الملف وإنشاء رابط المعاينة للصورة
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setModelUrl(null); // إعادة تعيين المجسم السابق عند اختيار صورة جديدة
    }
  };

  // 2️⃣ إرسال الصورة إلى الـ Backend وتوليد المجسم 3D
  const handleSubmit = async () => {
    if (!selectedFile) {
      alert("الرجاء اختيار صورة أولاً!");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const backendHost = window.location.hostname;
      const baseUrl =
        process.env.NEXT_PUBLIC_API_URL || `http://${backendHost}:8000`;

      // المسار الصحيح والمطابق لـ FastAPI Router مع /api/v1
      const response = await fetch(`${baseUrl}/api/v1/generate-from-image`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("فشل التوليد من السيرفر");
      }

      const data = await response.json();
      
      // تركيب رابط الـ GLB النهائي
      const fullModelUrl = `${baseUrl}${data.model_url}`;
      setModelUrl(fullModelUrl);
    } catch (error) {
      console.error("حدث خطأ أثناء التوليد:", error);
      alert("حدث خطأ أثناء الاتصال بالـ Backend، أعد المحاولة.");
    } finally {
      setLoading(false);
    }
  };

  // 3️⃣ دالة تنزيل ملف الـ GLB مباشرة للجهاز
  const handleDownload = async () => {
    if (!modelUrl) return;
    try {
      const response = await fetch(modelUrl);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `3d_model_${Date.now()}.glb`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("فشل التنزيل:", err);
      alert("حدث خطأ أثناء تنزيل الملف.");
    }
  };

  return (
    <main
      className="min-h-screen bg-black text-white p-6 md:p-12 flex flex-col items-center justify-center font-sans"
      dir="rtl"
    >
      {/* العنوان الوصفي */}
      <h1 className="text-3xl md:text-4xl font-bold mb-3 text-center bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
        منصة توليد الأيقونات والمجسمات 3D
      </h1>
      <p className="text-gray-400 mb-8 text-center text-sm md:text-base max-w-xl">
        حول صورك ثنائية الأبعاد إلى مجسمات ثلاثية الأبعاد باستخدام الذكاء الاصطناعي
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-5xl bg-gray-900/60 p-6 md:p-8 rounded-2xl border border-gray-800 backdrop-blur-md shadow-2xl">
        {/* القسم الأيمن: رفع الصورة والتحكم */}
        <div className="flex flex-col justify-between space-y-6">
          <div className="flex flex-col items-center justify-center">
            <span className="text-sm font-semibold text-gray-300 mb-3 w-full text-right">
              1. اختيار ومعاينة الصورة
            </span>

            {/* منطقة معاينة الصورة المختارة */}
            <div className="w-full h-64 border-2 border-dashed border-gray-700 hover:border-blue-500/70 transition-colors rounded-xl flex items-center justify-center bg-gray-800/30 overflow-hidden relative p-2">
              {previewUrl ? (
                <img
                  src={previewUrl}
                  alt="معاينة الصورة"
                  className="max-w-full max-h-full object-contain rounded-lg"
                />
              ) : (
                <div className="text-center p-4">
                  <p className="text-gray-400 text-sm">
                    قم برفع صورة لتوليد المجسم هنا
                  </p>
                  <p className="text-gray-600 text-xs mt-1">(JPG, PNG)</p>
                </div>
              )}
            </div>
          </div>

          {/* مدخل الملفات المخفي والأزرار */}
          <div className="space-y-3">
            <input
              type="file"
              ref={fileInputRef}
              accept="image/png, image/jpeg"
              className="hidden"
              onChange={handleFileChange}
            />

            <button
              onClick={() => fileInputRef.current?.click()}
              className="w-full bg-gray-800 hover:bg-gray-700 text-gray-200 border border-gray-700 font-medium py-3 px-6 rounded-xl transition-all text-center"
            >
              {selectedFile
                ? `تغيير الصورة (${selectedFile.name})`
                : "اختر صورة (JPG / PNG)"}
            </button>

            <button
              onClick={handleSubmit}
              disabled={!selectedFile || loading}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 disabled:from-gray-700 disabled:to-gray-800 text-white font-semibold py-3 px-6 rounded-xl transition-all shadow-lg shadow-blue-500/10 text-center"
            >
              {loading ? "جاري التوليد بواسطة AI..." : "توليد مجسم 3D"}
            </button>
          </div>
        </div>

        {/* القسم الأيسر: شاشة عرض الـ 3D والتحميل */}
        <div className="flex flex-col justify-between">
          <div>
            <span className="text-sm font-semibold text-gray-300 mb-3 w-full block text-right">
              2. عرض وتفحص المجسم ثلاثي الأبعاد
            </span>
            <div className="w-full h-[320px] rounded-xl overflow-hidden border border-gray-800 bg-gray-950/80 flex items-center justify-center relative">
              <ModelViewer modelUrl={modelUrl} />
            </div>
          </div>

          {/* زر تحميل الملف الـ 3D */}
          {modelUrl && (
            <button
              onClick={handleDownload}
              className="mt-4 w-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-3 px-6 rounded-xl transition-all shadow-lg shadow-emerald-500/20 text-center flex items-center justify-center gap-2"
            >
              <span>📥</span>
              <span>تحميل مجسم 3D (.glb)</span>
            </button>
          )}
        </div>
      </div>
    </main>
  );
}