# 🌕 LunarCraterDetection — Autonomous Planetary Computer Vision Pipeline

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![NumPy](https://img.shields.io/badge/NumPy-Scientific-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

An autonomous computer vision system designed for orbital lunar imagery analysis. It automates crater detection, diameter measurement, contour analysis, and topological coordinate extraction using multi-scale Hough Transforms and dynamic thresholding.

---

## 🛰️ System Architecture

```mermaid
graph LR
    A[Orbital Lunar Imagery / Live Map Stream] --> B[Selenium Tile Scraper]
    B --> C[Grayscale Conversion & Gaussian Blur]
    C --> D[Adaptive Canny Edge Detection]
    D --> E[Multi-Scale Hough Circle Transform]
    E --> F[False-Positive Noise Suppression]
    F --> G[Topological Extraction: Center (x, y), Radius, Area]
    G --> H[Annotated Visual Output & Planetary Map Export]
```

---

## 🌟 Key Capabilities

- **🎯 Multi-Scale Hough Circle Transform:** Configurable parameter tuning (`dp`, `minDist`, `param1`, `param2`, `minRadius`, `maxRadius`) for small impact craters and large multi-ring lunar basins.
- **🛰️ Live Satellite Stream Ingestion (`livecraterdetector.py`):** Selenium-driven orbital tile collector that extracts real-time imagery from web map coordinate systems.
- **⚡ Advanced Morphological Filtering (`powerfulcraterdetector.py`):** Multi-stage Gaussian blurring, CLAHE contrast equalization, and adaptive thresholding to eliminate solar shadow artifacts.
- **📊 Metric Extraction:** Computes crater centers, diameter estimation in pixels/kilometers, and density distribution.

---

## 📂 Repository Layout

```
LunarCraterDetection/
├── livecraterdetector.py      # Real-time satellite scraping & live circle detection pipeline
├── powerfulcraterdetector.py  # High-precision multi-pass morphological feature extractor
└── README.md                  # Comprehensive technical documentation
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9+
- Chrome / Chromium & ChromeDriver (for Selenium tile scraping)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/abhay2008/LunarCraterDetection.git
cd LunarCraterDetection

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install required packages
pip install opencv-python numpy selenium pillow requests
```

---

## 🚀 Usage

### 1. High-Precision Offline Crater Extraction
Run the comprehensive multi-pass feature extractor on local satellite imagery:
```bash
python powerfulcraterdetector.py
```

### 2. Live Orbital Tile Scraping & Stream Detection
Run real-time stream ingestion and live annotation:
```bash
python livecraterdetector.py
```

---

## 🌐 Connected Projects

- **Web Dashboard:** [CraterDetectionWebsite](https://github.com/abhay2008/CraterDetectionWebsite) — Interactive browser-based lunar map explorer.

---

## 👨‍💻 Author

**Abhay Kashyap**
- B.Tech in Electronics & Communication Engineering (ECE), B.M.S. College of Engineering (BMSCE)
- GitHub: [@abhay2008](https://github.com/abhay2008)
