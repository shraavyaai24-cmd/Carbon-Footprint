import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Configure Gemini API
# -----------------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="TerraAI",
    page_icon="🌍",
    layout="centered"
)

# -----------------------------
# Title
# -----------------------------
st.title("🌍 TerraAI")
st.subheader("Interactive Carbon Footprint Assessment Chatbot")
st.markdown("### SDG 13: Climate Action")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🌱 About")
st.sidebar.info(
    """
    TerraAI helps users estimate their carbon footprint
    and provides eco-friendly suggestions based on lifestyle habits.
    """
)

# -----------------------------
# User Inputs
# -----------------------------
st.header("🚗 Transportation")

transport = st.selectbox(
    "Primary mode of transportation",
    [
        "Car",
        "Bike",
        "Bus",
        "Train",
        "Bicycle",
        "Walking"
    ]
)

distance = st.slider(
    "Average distance traveled daily (km)",
    0,
    100,
    10
)

flights = st.slider(
    "Number of flights taken yearly",
    0,
    20,
    0
)

# -----------------------------
# Electricity Section
# -----------------------------
st.header("⚡ Electricity Usage")

electricity_bill = st.slider(
    "Average monthly electricity bill (₹)",
    0,
    10000,
    2000
)

acs = st.slider(
    "Number of ACs used at home",
    0,
    5,
    1
)

led_usage = st.radio(
    "Do you use LED bulbs?",
    ["Yes", "No"]
)

# -----------------------------
# Food Habits
# -----------------------------
st.header("🍔 Food Habits")

diet = st.radio(
    "Diet type",
    ["Vegetarian", "Non-Vegetarian"]
)

meat_days = st.slider(
    "How many days per week do you eat meat?",
    0,
    7,
    2
)

food_waste = st.radio(
    "Do you waste food often?",
    ["Yes", "No"]
)

# -----------------------------
# Lifestyle & Waste
# -----------------------------
st.header("♻️ Lifestyle")

recycle = st.radio(
    "Do you recycle regularly?",
    ["Yes", "No"]
)

plastic_usage = st.selectbox(
    "Plastic usage frequency",
    [
        "Low",
        "Moderate",
        "High"
    ]
)

fast_fashion = st.selectbox(
    "How often do you buy fast fashion?",
    [
        "Rarely",
        "Sometimes",
        "Frequently"
    ]
)

# -----------------------------
# Calculate Button
# -----------------------------
if st.button("Calculate Carbon Footprint"):

    score = 0

    # -----------------------------
    # Transportation Score
    # -----------------------------
    if transport == "Car":
        score += 30
    elif transport == "Bike":
        score += 20
    elif transport == "Bus":
        score += 10
    elif transport == "Train":
        score += 8
    elif transport == "Bicycle":
        score += 2
    elif transport == "Walking":
        score += 1

    score += distance * 0.5
    score += flights * 10

    # -----------------------------
    # Electricity Score
    # -----------------------------
    score += electricity_bill / 200
    score += acs * 10

    if led_usage == "No":
        score += 10

    # -----------------------------
    # Food Score
    # -----------------------------
    if diet == "Non-Vegetarian":
        score += 15

    score += meat_days * 3

    if food_waste == "Yes":
        score += 10

    # -----------------------------
    # Lifestyle Score
    # -----------------------------
    if recycle == "No":
        score += 10

    if plastic_usage == "Moderate":
        score += 10
    elif plastic_usage == "High":
        score += 20

    if fast_fashion == "Sometimes":
        score += 10
    elif fast_fashion == "Frequently":
        score += 20

    # -----------------------------
    # Result Category
    # -----------------------------
    st.header("📊 Your Result")

    if score < 50:
        category = "Low Carbon Footprint 🌱"
        color = "green"

    elif score < 100:
        category = "Moderate Carbon Footprint ⚠️"
        color = "orange"

    else:
        category = "High Carbon Footprint 🔥"
        color = "red"

    st.markdown(f"## Score: {round(score, 2)}")
    st.markdown(f"### {category}")

    # -----------------------------
    # AI Suggestions
    # -----------------------------
    prompt = f"""
    The user has a carbon footprint score of {score}.

    User details:
    - Transport: {transport}
    - Daily distance: {distance} km
    - Flights yearly: {flights}
    - Electricity bill: {electricity_bill}
    - ACs used: {acs}
    - LED usage: {led_usage}
    - Diet: {diet}
    - Meat consumption: {meat_days} days/week
    - Food waste: {food_waste}
    - Recycling: {recycle}
    - Plastic usage: {plastic_usage}
    - Fast fashion: {fast_fashion}

    Give:
    1. A short analysis of their lifestyle
    2. 5 personalized eco-friendly suggestions
    3. Motivational advice for sustainable living

    Keep the response simple and friendly.
    """

    response = model.generate_content(prompt)

    st.header("🤖 TerraAI Suggestions")

    st.write(response.text)

    # -----------------------------
    # SDG Section
    # -----------------------------
    st.success(
        "This project supports SDG 13: Climate Action 🌍"
    )
