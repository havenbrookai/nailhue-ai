
import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import json
import io

# Load polish color database
with open("nail_polish_color_database.json", "r") as f:
    polish_db = json.load(f)

# Helper functions
def hex_to_rgb(hex_val):
    hex_val = hex_val.lstrip('#')
    return tuple(int(hex_val[i:i+2], 16) for i in (0, 2, 4))

def color_distance(rgb1, rgb2):
    return sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)) ** 0.5

def find_closest_polish(user_hex):
    user_rgb = hex_to_rgb(user_hex)
    best_match = None
    smallest_diff = float('inf')
    for polish in polish_db:
        polish_rgb = hex_to_rgb(polish['hex'])
        diff = color_distance(user_rgb, polish_rgb)
        if diff < smallest_diff:
            smallest_diff = diff
            best_match = polish
    return best_match

def extract_dominant_color(image, k=3):
    image = image.resize((150, 150))
    image_np = np.array(image)
    image_np = image_np.reshape((-1, 3))
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(image_np)
    dominant_color = kmeans.cluster_centers_[0].astype(int)
    return '#{:02x}{:02x}{:02x}'.format(*dominant_color)

# Streamlit UI
st.title("💅 NailHue AI")
st.write("Upload your nail inspo photo. We'll find the closest real polish match!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    hex_color = extract_dominant_color(image)
    match = find_closest_polish(hex_color)

    st.markdown(f"### 🎨 Detected Color: `{hex_color}`")
    st.markdown(f"### ✅ Closest Match: **{match['brand']} – {match['shade']}**")
    st.markdown(f"<div style='background-color:{match['hex']}; width:100px; height:30px; border-radius:5px;'></div>", unsafe_allow_html=True)
    st.markdown(f"[🔗 View Product]({match['link']})", unsafe_allow_html=True)
