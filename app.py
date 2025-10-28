from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd

# Load ML model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI(
    title="FitPredict API",
    description="AI-powered fitness level prediction API",
    version="1.0.0"
)

# Define region/city categories
tier_1_cities = ["New York", "Los Angeles", "Chicago", "Houston", "Miami", "San Francisco", "Dallas"]
tier_2_cities = [
    "Seattle", "Boston", "Denver", "Atlanta", "San Diego", "Phoenix", "Austin", "Portland",
    "Tampa", "Minneapolis", "Detroit", "Charlotte", "Las Vegas", "Philadelphia", "Nashville",
    "Kansas City", "Indianapolis", "Cleveland", "Baltimore", "Orlando"
]

# Pydantic model for input validation
class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=100, description="Age of the member")]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kilograms")]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description="Height in meters")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Annual income in LPA")]
    city: Annotated[str, Field(..., description="City of residence")]
    occupation: Annotated[
        Literal["student", "software_engineer", "teacher", "freelancer", "business_owner", 
                "entrepreneur", "private_job", "government_job", "manager", "unemployed", "retired"],
        Field(..., description="Occupation type")
    ]

    # Computed fields
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def income_category(self) -> str:
        if self.income_lpa < 10:
            return "low"
        elif self.income_lpa < 30:
            return "medium"
        else:
            return "high"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 18:
            return "teen"
        elif self.age < 30:
            return "young_adult"
        elif self.age < 50:
            return "adult"
        return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3


@app.get("/")
def home():
    """Root endpoint - API information"""
    return {
        "name": "FitPredict API",
        "version": "1.0.0",
        "description": "AI-powered fitness level prediction API",
        "endpoints": {
            "/": "API information",
            "/health": "Health check",
            "/predict": "Make fitness predictions (POST)",
            "/docs": "Interactive API documentation"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "API is running",
        "model_loaded": model is not None
    }


@app.post("/predict")
def predict_membership(data: UserInput):
    """Predict fitness membership level based on user data"""
    try:
        # Prepare dataframe with features matching the trained model
        input_df = pd.DataFrame([{
            "bmi": data.bmi,
            "age_group": data.age_group,
            "income_category": data.income_category,
            "city_tier": data.city_tier,
            "occupation": data.occupation
        }])

        # Make prediction
        prediction = model.predict(input_df)[0]
        
        # Get prediction probabilities if available
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(input_df)[0]
            prob_dict = {cls: float(prob) for cls, prob in zip(model.classes_, probabilities)}
        else:
            prob_dict = {}

        return JSONResponse(status_code=200, content={
            "predicted_membership_category": prediction,
            "input_features": {
                "bmi": data.bmi,
                "age_group": data.age_group,
                "income_category": data.income_category,
                "city_tier": data.city_tier,
                "occupation": data.occupation
            },
            "probabilities": prob_dict
        })
    
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": "Prediction failed",
            "message": str(e)
        })
