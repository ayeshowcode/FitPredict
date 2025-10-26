import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Load the trained model
@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

# Feature engineering functions
def age_group(age):
    if age < 18:
        return 'teen'
    elif 18 <= age < 30:
        return 'young_adult'
    elif 30 <= age < 50:
        return 'adult'
    else:
        return 'senior'

def income_category(income):
    if income < 10:
        return 'low'
    elif 10 <= income < 30:
        return 'medium'
    else:
        return 'high'

def city_tier(city):
    tier_1_cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "San Antonio", 
                     "San Diego", "Dallas", "San Francisco", "Seattle", "Boston", "Miami"]
    tier_2_cities = [
        "Denver", "Atlanta", "Portland", "Austin",
        "Tampa", "Minneapolis", "Detroit", "Charlotte", "Las Vegas", "Philadelphia", "Nashville",
        "Kansas City", "Indianapolis", "Cleveland", "Baltimore", "Orlando"
    ]
    
    if city in tier_1_cities:
        return 1
    elif city in tier_2_cities:
        return 2
    else:
        return 3

# Streamlit App
def main():
    st.set_page_config(page_title="Fitness Level Predictor", page_icon="💪", layout="wide")
    
    st.title("💪 Fitness Level Prediction App")
    st.markdown("### Predict your fitness level based on personal and lifestyle data")
    st.divider()
    
    # Load model
    try:
        model = load_model()
    except FileNotFoundError:
        st.error("❌ Model file not found! Please ensure 'model.pkl' exists in the directory.")
        return
    
    # Create two columns for input layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Personal Information")
        age = st.number_input("Age", min_value=15, max_value=100, value=30, step=1)
        weight = st.number_input("Weight (kg)", min_value=40.0, max_value=200.0, value=70.0, step=0.1)
        height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75, step=0.01)
        
        # Calculate and display BMI
        bmi = weight / (height ** 2)
        st.metric("Calculated BMI", f"{bmi:.2f}")
    
    with col2:
        st.subheader("🏙️ Lifestyle Information")
        income_lpa = st.number_input("Annual Income (LPA)", min_value=0.0, max_value=100.0, value=15.0, step=0.5)
        
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "San Diego", 
                  "Dallas", "San Francisco", "Seattle", "Boston", "Miami", "Denver", 
                  "Atlanta", "Portland", "Las Vegas", "Orlando", "Philadelphia"]
        city = st.selectbox("City", sorted(cities))
        
        occupations = ["student", "software_engineer", "teacher", "freelancer", "business_owner",
                      "entrepreneur", "private_job", "government_job", "manager", "unemployed", "retired"]
        occupation = st.selectbox("Occupation", sorted(occupations))
    
    st.divider()
    
    # Prediction button
    if st.button("🔮 Predict Fitness Level", type="primary", use_container_width=True):
        # Prepare input data
        age_grp = age_group(age)
        income_cat = income_category(income_lpa)
        city_tr = city_tier(city)
        
        # Create dataframe with features in the correct order
        input_data = pd.DataFrame({
            'bmi': [bmi],
            'age_group': [age_grp],
            'income_category': [income_cat],
            'city_tier': [city_tr],
            'occupation': [occupation]
        })
        
        # Make prediction
        try:
            prediction = model.predict(input_data)[0]
            
            # Display result with styling
            st.success("### Prediction Results")
            
            result_col1, result_col2, result_col3 = st.columns(3)
            
            with result_col1:
                st.metric("Predicted Fitness Level", prediction)
            
            with result_col2:
                st.metric("Age Group", age_grp.replace('_', ' ').title())
            
            with result_col3:
                st.metric("Income Category", income_cat.upper())
            
            # Additional info
            with st.expander("📋 View Input Features"):
                st.write(input_data)
            
            # Fitness level explanation
            st.divider()
            if prediction == "High":
                st.info("🏆 **High Fitness Level**: Great job! Keep maintaining your healthy lifestyle.")
            elif prediction == "Medium":
                st.warning("⚡ **Medium Fitness Level**: You're doing well! Consider increasing physical activity.")
            else:
                st.error("💪 **Low Fitness Level**: Consider consulting a fitness professional to improve your health.")
                
        except Exception as e:
            st.error(f"❌ Prediction error: {str(e)}")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>Built with Streamlit • Powered by Random Forest ML Model</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
