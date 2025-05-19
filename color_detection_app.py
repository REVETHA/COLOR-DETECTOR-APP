import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Color Detector", layout="centered")

# Load color dataset
@st.cache_data
def load_colors():
    return pd.read_csv("colors(first_done).csv")

color_data = load_colors()

# Get closest color name
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = "Unknown"
    for i in range(len(color_data)):
        r_d = abs(R - int(color_data.loc[i, "R"]))
        g_d = abs(G - int(color_data.loc[i, "G"]))
        b_d = abs(B - int(color_data.loc[i, "B"]))
        distance = r_d + g_d + b_d
        if distance < minimum:
            minimum = distance
            cname = color_data.loc[i, "color_name"]
    return cname

# Initialize session state to store detections
if "detections" not in st.session_state:
    st.session_state.detections = []

st.title("🎨 Kid-Friendly Color Detector")
st.write("Upload an image and click on any part of it to detect the color!")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Load and display image
    image = Image.open(uploaded_file).convert('RGB')
    img_array = np.array(image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.markdown("### Simulate a click by entering coordinates:")

    col1, col2 = st.columns(2)
    x = col1.number_input("X-coordinate", min_value=0, max_value=img_array.shape[1] - 1, step=1)
    y = col2.number_input("Y-coordinate", min_value=0, max_value=img_array.shape[0] - 1, step=1)

    if st.button("Detect Color"):
        b, g, r = img_array[int(y), int(x)]
        color_name = get_color_name(r, g, b)
        rgb = f"({r}, {g}, {b})"
        st.session_state.detections.append({
            "Color Name": color_name,
            "RGB": rgb,
            "Sample": f"rgb({r},{g},{b})"
        })

    # Display detected colors
    if st.session_state.detections:
        st.markdown("### 🎯 All Detected Colors")
        for det in st.session_state.detections:
            st.markdown(f"**Color Name:** {det['Color Name']}  |  **RGB:** {det['RGB']}")
            st.markdown(
                f"<div style='width: 100px; height: 50px; background-color: {det['Sample']}; border: 1px solid #000; margin-bottom:10px;'></div>",
                unsafe_allow_html=True
            )
