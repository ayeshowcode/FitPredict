from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd

# Load ML model
with open('fitness_model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

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
    active_lifestyle: Annotated[bool, Field(..., description="Does the member have an active lifestyle?")]
    city: Annotated[str, Field(..., description="City of residence")]
    occupation: Annotated[
        Literal["student", "office_worker", "self_employed", "retired", "athlete", "unemployed"],
        Field(..., description="Occupation type")
    ]

    # Computed fields
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def fitness_risk(self) -> str:
        if not self.active_lifestyle and self.bmi > 30:
            return "high_risk"
        elif self.bmi > 27 or not self.active_lifestyle:
            return "medium_risk"
        else:
            return "low_risk"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 40:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
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


@app.post("/predict")
def predict_membership(data: UserInput):
    # Prepare dataframe for prediction
    input_df = pd.DataFrame([{
        "bmi": data.bmi,
        "age_group": data.age_group,
        "fitness_risk": data.fitness_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }])

    # Predict using ML model
    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={"predicted_membership_category": prediction})
