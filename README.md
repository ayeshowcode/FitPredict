# FitPredict - AI-Powered Fitness Level Prediction System

An intelligent machine learning application that predicts fitness levels based on personal and lifestyle data. Built with scikit-learn, FastAPI, and Streamlit for comprehensive ML model deployment.

## 🎯 Overview

FitPredict uses a Random Forest classifier to predict fitness levels (High, Medium, Low) by analyzing demographic information, body metrics, and lifestyle factors. The system provides both a REST API and an interactive web interface for predictions.

## ✨ Features

- **Smart Feature Engineering**: Automatically computes BMI, age groups, income categories, and city tier classifications
- **High Accuracy**: Random Forest model with comprehensive preprocessing pipeline
- **Dual Interface**: RESTful API and interactive Streamlit dashboard
- **Real-time Predictions**: Instant fitness level assessment with confidence scores
- **Input Validation**: Robust Pydantic models ensure data quality
- **Responsive Design**: Clean, modern UI with intuitive user experience

## 📁 Project Structure

```
fitpredict/
├── data/
│   └── fitness_data.csv          # Training dataset
├── model/
│   └── model.pkl                 # Trained ML model (if using model/ directory)
├── fastapi.ipynb                 # Model training and experimentation notebook
├── streamlit_app.py              # Interactive web application
├── app.py                        # FastAPI REST API (optional)
├── requirements.txt              # Core dependencies
├── requirements-dev.txt          # Development dependencies
└── README.md                     # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/fitpredict.git
   cd fitpredict
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   
   For production:
   ```bash
   pip install -r requirements.txt
   ```
   
   For development (includes Streamlit, Jupyter):
   ```bash
   pip install -r requirements-dev.txt
   ```

## 💻 Usage

### Streamlit Web Application

Launch the interactive dashboard:

```bash
streamlit run streamlit_app.py
```

Navigate to `http://localhost:8501` in your browser.

**Features:**
- Input personal details (age, weight, height, income)
- Select city and occupation from dropdowns
- View BMI calculation automatically
- Get instant fitness level prediction with confidence scores
- See detailed breakdown of class probabilities

### Training the Model

Open and run the Jupyter notebook:

```bash
jupyter notebook fastapi.ipynb
```

The notebook includes:
- Data exploration and visualization
- Feature engineering (BMI, age groups, income categories, city tiers)
- Model training with RandomForestClassifier
- Model evaluation and performance metrics
- Model persistence to pickle file

## 🧠 Model Details

### Features

The model uses 5 engineered features:

1. **BMI (Body Mass Index)**: Calculated from weight and height
2. **Age Group**: Categorized as teen, young adult, adult, or senior
3. **Income Category**: 
   - Low: < ₹10 LPA
   - Medium: ₹10-30 LPA
   - High: ≥ ₹30 LPA
4. **City Tier**: 
   - Tier 1: Major metropolitan areas (NYC, LA, Chicago, etc.)
   - Tier 2: Secondary cities (Denver, Atlanta, Portland, etc.)
5. **Occupation**: Job category (student, engineer, teacher, etc.)

### Algorithm

- **Model**: Random Forest Classifier
- **Preprocessing**: OneHotEncoder for categorical features
- **Pipeline**: Integrated preprocessing and model training
- **Target Variable**: Fitness Level (High, Medium, Low)

### Performance

- Training/Test Split: 80/20
- Evaluation Metrics: Accuracy, Classification Report
- Cross-validation: Random state seeded for reproducibility

## 📊 Dataset

The training data includes:
- **100 samples** with diverse demographics
- **Features**: Age, weight, height, income, city, occupation
- **Target**: Fitness level classification
- **Coverage**: 16 US cities across multiple tiers

## 🛠️ Technologies

- **Machine Learning**: scikit-learn, pandas, numpy
- **Web Framework**: Streamlit, FastAPI (optional)
- **Data Processing**: pandas, OneHotEncoder
- **Model Persistence**: pickle
- **Development**: Jupyter Notebook

## 📦 Dependencies

### Core (`requirements.txt`)
```
pandas
scikit-learn
numpy
streamlit
```

### Development (`requirements-dev.txt`)
```
jupyter
notebook
matplotlib
seaborn
```

## 🔮 Future Enhancements

- [ ] Add more sophisticated feature engineering
- [ ] Implement model versioning and A/B testing
- [ ] Add data drift monitoring
- [ ] Expand dataset with more diverse samples
- [ ] Deploy to cloud platform (AWS, Azure, GCP)
- [ ] Add user authentication and history tracking
- [ ] Implement recommendation system based on predictions
- [ ] Add data visualization dashboard

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Dataset inspired by fitness industry research
- Built with modern ML best practices
- Designed for scalability and production deployment

## 📞 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ and Python**
