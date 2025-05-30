# solar_rooftop_ai_tool.py

import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io
import base64

st.set_page_config(page_title="Solar Rooftop Analysis Tool", layout="centered")
st.title("🌍 AI-Powered Solar Rooftop Assessment")

# Sidebar
st.sidebar.header("Upload Satellite Image")

uploaded_file = st.sidebar.file_uploader("Choose a rooftop image (JPEG/PNG)", type=["jpg", "jpeg", "png"])
location = st.sidebar.text_input("Location (City, Country)")
avg_sunlight = st.sidebar.slider("Average Sunlight Hours/Day", 1.0, 12.0, 6.0, 0.5)

# Constants for ROI Estimation
PANEL_EFFICIENCY = 0.18
SYSTEM_LOSS = 0.85  # accounts for shading, inverter loss, etc.
COST_PER_WATT = 1.2  # USD per watt
AVG_COST_PER_KWH = 0.15  # USD


def dynamic_rooftop_estimation(image):
    image_np = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area_estimate = 0
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) >= 4:
            area = cv2.contourArea(cnt)
            if area > 1000:
                area_estimate += area

    m2_estimate = round(area_estimate / 1000, 2)
    return m2_estimate


def calculate_solar_output(area_m2, sunlight_hours):
    usable_watt = area_m2 * 1000 * PANEL_EFFICIENCY * SYSTEM_LOSS
    daily_kwh = (usable_watt / 1000) * sunlight_hours
    yearly_kwh = daily_kwh * 365
    return daily_kwh, yearly_kwh, usable_watt


def calculate_roi(yearly_kwh, usable_watt):
    installation_cost = usable_watt * COST_PER_WATT
    annual_savings = yearly_kwh * AVG_COST_PER_KWH
    payback_period = installation_cost / annual_savings if annual_savings != 0 else float('inf')
    return installation_cost, annual_savings, payback_period


if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Rooftop Image", use_column_width=True)

    with st.spinner("Analyzing rooftop..."):
        usable_area = dynamic_rooftop_estimation(image)
        daily_kwh, yearly_kwh, usable_watt = calculate_solar_output(usable_area, avg_sunlight)
        installation_cost, annual_savings, payback_period = calculate_roi(yearly_kwh, usable_watt)

    st.success("Analysis Complete!")
    st.subheader("☀️ Solar Installation Report")
    st.markdown(f"**Location**: {location}")
    st.markdown(f"**Usable Rooftop Area**: {usable_area} m²")
    st.markdown(f"**Estimated Daily Output**: {daily_kwh:.2f} kWh")
    st.markdown(f"**Estimated Yearly Output**: {yearly_kwh:.2f} kWh")
    st.markdown(f"**Estimated Annual Savings**: ${annual_savings:.2f}")
    st.markdown(f"**Estimated Installation Cost**: ${installation_cost:.2f}")
    st.markdown(f"**Payback Period**: {payback_period:.1f} years")

    st.info("Note: This is a basic edge-based approximation. For production, use ML segmentation models.")
else:
    st.warning("Please upload a rooftop satellite image to begin analysis.")
