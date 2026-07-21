# 🚀 3D AI Generation Engine (FastAPI Backend)

A high-performance, lightweight FastAPI backend engineered for generating 3D models (`.glb`/`.obj`) from 2D images. Designed for seamless local execution and production deployment with optimal resource efficiency.

---

## 🎯 Overview

This repository hosts the backend core of the **3D AI Generation Engine**. It exposes RESTful APIs to ingest images, handle foreground/background segmentation, generate textured 3D meshes using modern graphics and machine learning utilities, and serve static outputs over fast asynchronous streams.

---

## ✨ Key Features

- **⚡ Fast & Asynchronous**: Built on top of **FastAPI** and **Uvicorn** for maximum throughput.
- **🎨 Automated Image Pre-processing**: Built-in background removal leveraging `rembg` and `onnxruntime`.
- **📦 3D Mesh Generation & Processing**: Generates and exports standard 3D file formats (`.glb`) ready for AR/VR and web viewers.
- **🌐 Static Asset Hosting**: Mounted static directory (`/outputs`) providing direct HTTP access to generated 3D files.
- **🛡️ Production-Ready Environment**: Configured with CORS middleware for seamless integration with frontend frameworks (Flutter, React, Three.js, etc.).
- **🧹 Zero-Leak Memory Management**: Automatic cleanup of transient files and garbage collection after every generation cycle.

---

## 🛠️ Tech Stack & Dependencies

- **Framework**: FastAPI, Uvicorn
- **AI & Graphics Tools**: `rembg`, `onnxruntime`, `trimesh`, `Pillow`, `PyMCubes`, `transformers`, `imageio`
- **Utility**: Pydantic, Python-Multipart, Requests

---

## 📁 Project Structure

```text
├── app/
│   ├── main.py            # Main FastAPI Application & Endpoints
│   ├── api/               # API Routes & Controllers
│   └── outputs/           # Local storage for generated 3D assets
├── requirements.txt       # Project Dependencies
└── README.md              # Project Documentation
