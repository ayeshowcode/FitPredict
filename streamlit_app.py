import streamlit as st
import requests

API_URL = "http://16.171.43.225:8000/predict" 

st.title("Fitness Level Predictor")
st.markdown("Enter your details below:")

# Input fields
age = st.number_input("Age", min_value=1, max_value=100, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.72)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
city = st.text_input("City", value="Houston")
occupation = st.selectbox(
    "Occupation",
    ['student', 'software_engineer', 'teacher', 'freelancer', 'business_owner', 
     'entrepreneur', 'private_job', 'government_job', 'manager', 'unemployed', 'retired']
)

if st.button("Predict Fitness Level"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if response.status_code == 200 and "predicted_membership_category" in result:
            prediction = result["predicted_membership_category"]
            st.success(f"Predicted Fitness Level: **{prediction}**")
            
            if "input_features" in result:
                st.write("📊 Computed Features:")
                st.json(result["input_features"])
            
            if "probabilities" in result and result["probabilities"]:
                st.write("📈 Class Probabilities:")
                st.json(result["probabilities"])

        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
