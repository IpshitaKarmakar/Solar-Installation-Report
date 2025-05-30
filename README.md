# Solar-Installation-Report
Solar Rooftop AI Tool

This document explains the core structure and logic behind the Streamlit-based AI project for solar rooftop analysis.

File Structure

solar-rooftop-ai/
├── solar_rooftop_ai_tool.py     # Main application
├── requirements.txt             # Python dependencies
└── README.md                    # Documentation

Code Explanation: solar_rooftop_ai_tool.py

import streamlit as st
import numpy as np
import cv2
from PIL import Image

Streamlit: Used to create an interactive web UI.

NumPy: Handles array-based image data.

OpenCV (cv2): Performs edge detection and contour analysis.

Pillow (PIL): Handles uploaded image formats.

📍 Page Configuration

st.set_page_config(page_title="Solar Rooftop Analysis Tool", layout="centered")
st.title("🌍 AI-Powered Solar Rooftop Assessment")

Sets the browser title and main app title.

🖼️ Sidebar Input

uploaded_file = st.sidebar.file_uploader("Choose a rooftop image (JPEG/PNG)", type=["jpg", "jpeg", "png"])
location = st.sidebar.text_input("Location (City, Country)")
avg_sunlight = st.sidebar.slider("Average Sunlight Hours/Day", 1.0, 12.0, 6.0, 0.5)

User uploads a satellite image.

Enters location and average sunlight to customize ROI.

⚙️ Constants

PANEL_EFFICIENCY = 0.18
SYSTEM_LOSS = 0.85
COST_PER_WATT = 1.2
AVG_COST_PER_KWH = 0.15

These define technical and financial parameters used in energy and ROI calculations.

📏 Rooftop Estimation

def dynamic_rooftop_estimation(image):

Converts the image to grayscale.

Applies edge detection using Canny algorithm.

Finds contours, filters small/noisy areas, and estimates the usable rooftop area in m².

🔋 Solar Output Calculation

def calculate_solar_output(area_m2, sunlight_hours):

Calculates usable wattage:

usable_watt = area × 1000 × efficiency × system_loss

Computes daily/yearly energy production in kWh.

💰 ROI Calculation

def calculate_roi(yearly_kwh, usable_watt):

Calculates:

Installation cost: watts × cost/watt

Annual savings: yearly_kwh × electricity rate

Payback: cost ÷ savings

🧾 Report Display

st.markdown(f"**Usable Rooftop Area**: {usable_area} m²")
st.markdown(f"**Payback Period**: {payback_period:.1f} years")

Displays detailed metrics: area, output, savings, cost, and payback.

requirements.txt

streamlit
numpy
opencv-python-headless
Pillow

Install using: pip install -r requirements.txt

🚀 Run Locally

git clone https://github.com/YOUR_USERNAME/solar-rooftop-ai.git
cd solar-rooftop-ai
pip install -r requirements.txt
streamlit run solar_rooftop_ai_tool.py

📚 Final Notes

Works best with top-down satellite rooftop images.

This prototype uses basic computer vision.

Can be extended using deep learning (SAM/YOLO).
