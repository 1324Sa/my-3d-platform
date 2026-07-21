"use client";

import React, { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, useGLTF, Center, Environment, Html } from "@react-three/drei";

interface ModelViewerProps {
  modelUrl: string | null;
}

// مكون فرعي لتحميل وعرض نموذج GLB
function Model({ url }: { url: string }) {
  const { scene } = useGLTF(url);
  return (
    <Center top>
      <primitive object={scene} scale={1.5} />
    </Center>
  );
}

export default function ModelViewer({ modelUrl }: ModelViewerProps) {
  if (!modelUrl) {
    return (
      <div className="w-full h-full min-h-[350px] flex items-center justify-center bg-gray-950 text-gray-500 text-sm rounded-xl border border-gray-800">
        قم برفع صورة لتوليد المجسم هنا
      </div>
    );
  }

  return (
    <div className="w-full h-full min-h-[350px] bg-gray-950 rounded-xl border border-gray-800 overflow-hidden relative">
      <Canvas camera={{ position: [0, 2, 5], fov: 45 }}>
        {/* إضاءة محيطية وموجهة لتفاصيل الظل والبريق */}
        <ambientLight intensity={1.2} />
        <directionalLight position={[10, 10, 10]} intensity={1.5} />
        <directionalLight position={[-10, -10, -10]} intensity={0.5} />
        <pointLight position={[0, 5, 0]} intensity={1} />

        <Suspense
          fallback={
            <Html center>
              <div className="text-blue-400 text-sm animate-pulse whitespace-nowrap">
                جاري تحميل المجسم...
              </div>
            </Html>
          }
        >
          <Model url={modelUrl} />
          <Environment preset="city" />
        </Suspense>

        {/* أدوات التحكم بالماوس: تدوير، تكبير، وتحريك */}
        <OrbitControls
          makeDefault
          enableZoom={true}
          enablePan={true}
          enableRotate={true}
          autoRotate={false}
          minDistance={1}
          maxDistance={20}
        />
      </Canvas>

      {/* إرشاد سريع للمستخدم */}
      <span className="absolute bottom-2 right-2 text-[10px] text-gray-400 bg-black/60 px-2 py-1 rounded border border-gray-800 backdrop-blur-sm pointer-events-none">
        🖱️ اسحب للتدوير | عجلة الماوس للتكبير
      </span>
    </div>
  );
}