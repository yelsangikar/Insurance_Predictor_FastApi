import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

# Store token in session state
if "token" not in st.session_state:
    st.session_state["token"] = None

st.title("Insurance Premium category predictions")

# --- AUTH SECTION ---
st.header("🔐 User Authentication")
auth_option = st.radio("Choose action", ["Register", "Login"])
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if auth_option == "Register":
    if st.button("Register"):
        try:
            r = requests.post(f"{BASE_URL}/register", params={"username": username, "password": password})
            if r.status_code == 200:
                st.success("✅ Registered successfully! Please log in.")
            else:
                st.error(f"❌ {r.json()['detail']}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Server not reachable.")
else:
    if st.button("Login"):
        try:
            r = requests.post(f"{BASE_URL}/login", data={"username": username, "password": password})
            if r.status_code == 200:
                st.session_state["token"] = r.json()["access_token"]
                st.success("✅ Logged in!")
            else:
                st.error("❌ Incorrect username or password")
        except requests.exceptions.ConnectionError:
            st.error("❌ Server not reachable.")

# --- PREDICTION SECTION ---
if st.session_state["token"]:
    st.header("📝 Enter your details below")

    age = st.number_input("Age", min_value=1, max_value=119, value=30)
    weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
    height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
    income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
    smoker = st.selectbox("Are you a smoker?", options=[True, False])
    city = st.text_input("City", value="Mumbai")
    occupation = st.selectbox(
        "Occupation",
        ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job']
    )

    if st.button("Predict Premium Category"):
        input_data = {
            "age": age,
            "weight": weight,
            "height": height,
            "income_lpa": income_lpa,
            "smoker": smoker,
            "city": city,
            "occupation": occupation
        }

        try:
            headers = {"Authorization": f"Bearer {st.session_state['token']}"}
            r = requests.post(f"{BASE_URL}/predict", json=input_data, headers=headers)

            if r.status_code == 200:
                result = r.json()
                prediction_data = result["response"]
                prediction = prediction_data["predicted_category"]
                confidence = prediction_data["confidence"]
                probs = prediction_data["class_probabilities"]

                st.success(f"Predicted Insurance Premium Category: **{prediction}**")
                st.info(f"Confidence: {confidence * 100:.2f}%")
                st.subheader("Class Probabilities:")
                st.json(probs)
            else:
                st.error(f"❌ {r.json().get('detail', 'Prediction failed')}")

        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the FastAPI server.")
        else:
            st.info("ℹ️ Please log in to access the prediction.")