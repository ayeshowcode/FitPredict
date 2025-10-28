# FitPredict - AI Fitness Level Prediction

Predict fitness levels (High, Medium, Low) using machine learning based on personal and lifestyle data.

## 📸 Screenshots

<div align="center">
  <img src="screenshots/image1.png" alt="FitPredict Interface" width="45%">
  <img src="screenshots/image2.png" alt="Prediction Results" width="45%">
</div>


## ⚡ Quick Start

### Using Streamlit (Local)
```bash
# Install dependencies
pip install -r requirements-dev.txt

# Run the Streamlit app
streamlit run streamlit_app.py
```

### Using Docker (FastAPI)
```bash
# Pull the Docker image
docker pull ayeshowcode/fitpredict-api

# Run the container
docker run -p 8000:8000 ayeshowcode/fitpredict-api
```

### Live Demo
- **FastAPI Docs**: http://your-aws-url:8000/docs
- **Streamlit App**: Connect to API at `http://localhost:8000`

Open `http://localhost:8501` (Streamlit) or `http://localhost:8000/docs` (FastAPI) in your browser.

## 🎯 Features

- 💪 **Smart Predictions** - Predicts fitness level from age, weight, height, income, city, and occupation
- 📊 **Automatic Feature Engineering** - Calculates BMI and categorizes age groups, income, and city tiers
- 🎨 **Dual Interface** - Streamlit web UI + FastAPI REST API
- 🐳 **Docker Support** - Containerized FastAPI deployment ready for production
- ☁️ **Cloud Ready** - Deployed on AWS with scalable architecture
- 🤖 **Machine Learning Model** - Random Forest classifier with 80%+ accuracy
- 📈 **Confidence Scores** - See prediction confidence and class probabilities
- ✅ **Input Validation** - Pydantic schema validation with computed fields

## 📁 Project Structure

```
├── data/
│   └── fitness_data.csv        # Training dataset (100 samples)
├── screenshots/                # Application screenshots
├── app.py                      # FastAPI REST API
├── streamlit_app.py            # Streamlit web interface
├── fastapi.ipynb               # Model training & experimentation
├── model.pkl                   # Trained ML model
├── Dockerfile                  # Docker configuration for FastAPI
├── requirements.txt            # Core dependencies (Docker)
├── requirements-dev.txt        # Development dependencies
└── README.md                   # Documentation
```

## 🧠 How It Works

The model analyzes personal and lifestyle data through 5 engineered features:

| Feature | Description | Categories |
|---------|-------------|------------|
| **BMI** | Body Mass Index | Calculated from weight/height |
| **Age Group** | Age category | Teen, Young Adult, Adult, Senior |
| **Income Category** | Income bracket | Low (<₹10L), Medium (₹10-30L), High (≥₹30L) |
| **City Tier** | City classification | Tier 1 (major metros), Tier 2 (secondary cities) |
| **Occupation** | Job category | Student, Engineer, Teacher, etc. |

### Model Details

- **Algorithm**: Random Forest Classifier (100 estimators)
- **Preprocessing**: OneHotEncoder for categorical variables
- **Pipeline**: Integrated preprocessing and prediction
- **Training Split**: 80/20 train-test split
- **Target Classes**: High, Medium, Low fitness levels

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ayeshowcode/ashok-fitness.git
   cd ashok-fitness
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

## 💻 Usage

### FastAPI REST API

**Run locally:**
```bash
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**API Endpoints:**
- `GET /` - API information
- `GET /health` - Health check
- `POST /predict` - Make predictions

**Example Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 31,
    "weight": 91,
    "height": 1.72,
    "income_lpa": 10,
    "city": "Houston",
    "occupation": "retired"
  }'
```

**Response:**
```json
{
  "predicted_membership_category": "Medium",
  "input_features": {
    "bmi": 30.78,
    "age_group": "adult",
    "income_category": "medium",
    "city_tier": 1,
    "occupation": "retired"
  },
  "probabilities": {
    "High": 0.25,
    "Medium": 0.60,
    "Low": 0.15
  }
}
```

### Streamlit Web Interface

1. Open the app at `http://localhost:8501`
2. Enter your details:
   - Personal info (age, weight, height)
   - Income level (in LPA)
   - Select city from dropdown
   - Choose occupation
3. Click "Predict Fitness Level"
4. View results with confidence scores and recommendations

### Training Your Own Model

Open and run the Jupyter notebook:

```bash
jupyter notebook fastapi.ipynb
```

The notebook walks through:
- Loading and exploring the dataset
- Feature engineering and preprocessing
- Training the Random Forest model
- Evaluating model performance
- Saving the model to `model.pkl`

## 🛠️ Tech Stack

- **Machine Learning**: scikit-learn, pandas, numpy
- **Web Frameworks**: FastAPI (REST API), Streamlit (UI)
- **Server**: Uvicorn (ASGI server)
- **Validation**: Pydantic (schema validation with computed fields)
- **Containerization**: Docker
- **Cloud Platform**: AWS EC2
- **Data Processing**: pandas, OneHotEncoder, ColumnTransformer
- **Model Persistence**: pickle
- **Development**: Jupyter Notebook

## 📊 Dataset

The model is trained on a curated fitness dataset with:
- **100 samples** across diverse demographics
- **7 input features**: age, weight, height, income, city, occupation, smoker
- **16 US cities** (Tier 1: NYC, LA, Chicago, etc.; Tier 2: Denver, Atlanta, etc.)
- **Target variable**: Fitness Level (High, Medium, Low)

## 🐳 Docker Deployment

### Build and Run Locally

```bash
# Build the Docker image
docker build -t fitpredict-api .

# Run the container
docker run -p 8000:8000 fitpredict-api
```

### Using Docker Hub

```bash
# Pull the image
docker pull ayeshowcode/fitpredict-api

# Run the container
docker run -p 8000:8000 ayeshowcode/fitpredict-api
```

### Docker Compose (Optional)

```yaml
version: '3.8'
services:
  api:
    image: ayeshowcode/fitpredict-api
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## ☁️ AWS Deployment

### Prerequisites
- AWS Account
- EC2 instance (t2.micro or higher)
- Security group with port 8000 open

### Deployment Steps

1. **Launch EC2 Instance**
   ```bash
   # Amazon Linux 2 or Ubuntu
   # Configure security group: Allow TCP port 8000
   ```

2. **Install Docker on EC2**
   ```bash
   # Amazon Linux 2
   sudo yum update -y
   sudo yum install docker -y
   sudo service docker start
   sudo usermod -a -G docker ec2-user
   
   # Ubuntu
   sudo apt-get update
   sudo apt-get install docker.io -y
   ```

3. **Pull and Run Container**
   ```bash
   docker pull ayeshowcode/fitpredict-api
   docker run -d -p 8000:8000 --name fitpredict ayeshowcode/fitpredict-api
   ```

4. **Access API**
   ```
   http://your-ec2-public-ip:8000/docs
   ```

### Production Considerations

- Use **Elastic Load Balancer** for high availability
- Set up **Auto Scaling Group** for traffic spikes
- Use **AWS ECR** for private container registry
- Configure **CloudWatch** for monitoring and logs
- Add **Route 53** for custom domain
- Enable **HTTPS** with AWS Certificate Manager
- Use **RDS** if switching to database storage




## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Ayesh** - [@ayeshowcode](https://github.com/ayeshowcode)

---

