# 🌍 Karachi AQI Forecasting System

A production-oriented Machine Learning system for forecasting the next-day Air Quality Index (AQI) for Karachi, Pakistan.

The system combines historical air quality data with live air quality data, performs automated feature engineering, stores the latest features in a Feast Feature Store, and generates AQI predictions through a FastAPI service using a trained Random Forest model.

The entire application is containerized using Docker and includes an automated scheduler for continuously updating live features.

---

# 🚀 Project Overview

Air pollution is a major environmental concern in Karachi. AQI values can change based on multiple environmental factors such as:

- PM2.5
- PM10
- Carbon Monoxide
- Nitrogen Dioxide
- Sulphur Dioxide
- Ozone
- Dust
- UV Index
- Historical AQI values

This project predicts the **next-day AQI for Karachi** using Machine Learning and a production-style data pipeline.

---

# 🏗️ System Architecture

```text
                    Historical AQI Data
                           │
                           ▼
                    Data Preprocessing
                           │
                           ▼
                    Feature Engineering
                           │
                           │
Live Air Quality API ──────┤
                           │
                           ▼
                 Combined Feature Pipeline
                           │
                           ▼
                   21 Model Features
                           │
                           ▼
                    Feast Feature Store
                           │
                           ▼
                    Random Forest Model
                           │
                           ▼
                       FastAPI
                           │
                           ▼
                    AQI Prediction API
                           │
                           ▼
                 Future Web Dashboard
```

---

# 🤖 Machine Learning Model

The project uses a **Random Forest Regressor** for AQI forecasting.

The model predicts the next-day AQI using environmental, temporal, and historical features.

## Model Features

The system uses **21 features**, including:

### Air Quality Features

- PM2.5
- PM10
- Carbon Monoxide
- Nitrogen Dioxide
- Sulphur Dioxide
- Ozone
- Aerosol Optical Depth
- Dust
- UV Index
- European AQI

### Time Features

- Year
- Month
- Day
- Day of Week

### Historical AQI Features

- AQI Lag 1
- AQI Lag 3
- AQI Lag 7
- AQI Rolling Mean 3
- AQI Rolling Mean 7
- AQI Rolling Standard Deviation 7

---

# 📊 Model Performance

The Random Forest model was evaluated using historical Karachi AQI data.

## Final Test Results

| Metric | Score |
|--------|-------|
| MAE | 7.36 |
| RMSE | 10.31 |
| R² Score | 0.81 |

The model achieved significantly better performance compared to the baseline approach.

---

# 🔄 Live Feature Pipeline

The system does not rely only on static historical data.

A live feature pipeline retrieves current air quality data and combines it with historical data.

## Pipeline

```text
Open-Meteo Air Quality API
          │
          ▼
Fetch Latest AQI Data
          │
          ▼
Combine Historical + Live Data
          │
          ▼
Feature Engineering
          │
          ▼
Create 21 Model Features
          │
          ▼
Push Features to Feast
          │
          ▼
Random Forest Prediction
```

---

# 🧠 Feature Store

The project uses **Feast** as a Feature Store.

Feast manages the latest features required by the Machine Learning model.

## Why Feast?

Feast helps ensure that the features used during prediction follow the same feature structure used during model training.

The system retrieves the latest features directly from Feast before generating a prediction.

```text
Feature Pipeline
      │
      ▼
Feast Feature Store
      │
      ▼
Prediction Service
      │
      ▼
Random Forest Model
```

---

# ⚡ FastAPI Service

The Machine Learning model is exposed through a FastAPI application.

FastAPI allows the AQI forecasting system to be accessed through REST API endpoints.

---

# 📡 API Endpoints

## Home Endpoint

```text
GET /
```

Response:

```json
{
    "message": "Karachi AQI Forecasting API is running",
    "status": "success"
}
```

---

## Health Check

```text
GET /health
```

Checks whether the API service is running.

Response:

```json
{
    "status": "healthy",
    "service": "Karachi AQI Forecasting API"
}
```

---

## Readiness Check

```text
GET /ready
```

Checks whether the system is ready to generate predictions.

It verifies:

- Model availability
- Feast Feature Store connection
- Latest features availability

Response:

```json
{
    "status": "ready",
    "model": "loaded",
    "feature_store": "connected",
    "features": "available"
}
```

---

## AQI Prediction

```text
GET /predict
```

This endpoint:

1. Retrieves the latest features from Feast.
2. Uses the trained Random Forest model.
3. Generates the AQI prediction.
4. Determines the AQI category.
5. Returns the prediction through the API.

Example response:

```json
{
    "city": "Karachi",
    "predicted_aqi": 61.63,
    "aqi_category": "Moderate",
    "prediction_for": "next day",
    "model": "Random Forest",
    "feature_store": "Feast"
}
```

---

# 🌡️ AQI Categories

The system converts predicted AQI values into understandable air quality categories.

| AQI Range | Category |
|----------|----------|
| 0 - 50 | Good |
| 51 - 100 | Moderate |
| 101 - 150 | Unhealthy for Sensitive Groups |
| 151 - 200 | Unhealthy |
| 201 - 300 | Very Unhealthy |
| 300+ | Hazardous |

---

# ⏱️ Automated Feature Scheduler

The system includes an automated scheduler.

The scheduler updates live air quality features every **6 hours**.

```text
Scheduler Starts
      │
      ▼
Fetch Live Air Quality Data
      │
      ▼
Combine with Historical Data
      │
      ▼
Generate Features
      │
      ▼
Push Latest Features to Feast
      │
      ▼
Wait 6 Hours
      │
      ▼
Repeat
```

The scheduler runs in a separate Docker container.

---

# 🐳 Docker Architecture

The project uses Docker and Docker Compose.

Two separate containers are used.

```text
Docker Compose
      │
      ├───────────────┐
      │               │
      ▼               ▼
 FastAPI API      Scheduler
 Container        Container
      │               │
      │               │
      ▼               ▼
 Prediction      Live Feature
 Service          Updates
      │               │
      └───────┬───────┘
              │
              ▼
       Feast Feature Store
              │
              ▼
       Persistent Storage
```

---

# 📦 Containers

## API Container

Runs the FastAPI application.

Responsibilities:

- Health checks
- Readiness checks
- AQI predictions
- API responses
- Error handling
- Logging

## Scheduler Container

Runs independently from the API.

Responsibilities:

- Fetch live AQI data
- Update features
- Push latest features to Feast
- Run automatically every 6 hours

---

# 💾 Persistent Storage

Docker volumes are used to preserve Feast data.

This ensures that feature store data remains available even when containers restart.

```text
Container Restart
       │
       ▼
Docker Volume
       │
       ▼
Feast Data Preserved
```

---

# 🧪 Testing

The project includes automated testing using Pytest.

Tests cover:

- Home endpoint
- Health endpoint
- Readiness endpoint
- Prediction endpoint
- AQI categories
- Error handling
- Prediction service

Run tests using:

```bash
pytest -v
```

---

# 🔐 Environment Variables

The project uses environment variables for configuration.

Example:

```env
CITY=Karachi
COUNTRY=Pakistan

LATITUDE=24.8607
LONGITUDE=67.0011

TIMEZONE=Asia/Karachi

API_PORT=8000

OPEN_METEO_BASE_URL=https://air-quality-api.open-meteo.com/v1/air-quality

SCHEDULER_INTERVAL_HOURS=6
```

Create your local environment file:

### Windows

```bash
copy .env.example .env
```

---

# 🛠️ Technologies Used

## Programming

- Python

## Machine Learning

- Scikit-learn
- Random Forest

## Data Processing

- Pandas
- NumPy

## Feature Engineering

- Custom Feature Pipeline

## Feature Store

- Feast

## API

- FastAPI
- Pydantic
- Uvicorn

## Live Data

- Open-Meteo Air Quality API

## Testing

- Pytest

## Containerization

- Docker
- Docker Compose

## Version Control

- Git
- GitHub

---

# 📁 Project Structure

```text
Karachi_AQI_Forecasting/
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   └── logger.py
│
├── src/
│   ├── config.py
│   ├── feature_engineering.py
│   ├── prediction_service.py
│   ├── push_features_to_feast.py
│   ├── get_features_from_feast.py
│   ├── predict_from_feast.py
│   ├── update_live_features.py
│   ├── run_live_prediction.py
│   └── scheduler.py
│
├── feature_repo/
│   └── feature_repo/
│       ├── feature_definitions.py
│       └── feature_store.yaml
│
├── notebooks/
│   ├── 01_data_preprocessing.ipynb
│   └── 02_realtime_feature_pipeline.ipynb
│
├── data/
│   └── raw/
│       └── air_quality/
│
├── test/
│   ├── test_api.py
│   └── test_prediction_service.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🚀 Running the Project

## Clone the Repository

```bash
git clone https://github.com/mubashir-azeem/karachi-aqi-forecasting.git
```

Move into the project directory:

```bash
cd karachi-aqi-forecasting
```

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configure Environment Variables

Create the environment file:

### Windows

```bash
copy .env.example .env
```

---

# 🐳 Run Using Docker

Build and start the application:

```bash
docker compose up --build -d
```

Check running containers:

```bash
docker ps
```

Expected containers:

```text
karachi-aqi-api
karachi-aqi-scheduler
```

---

# 📊 Access the API

Once running locally:

```text
http://localhost:8000
```

## Interactive API Documentation

FastAPI automatically provides interactive API documentation:

```text
http://localhost:8000/docs
```

---

# 🎨 Interactive Dashboard

## Coming Next

The next major phase of this project is the development of a professional interactive AQI Dashboard.

The dashboard will connect directly to the FastAPI backend and display real predictions from the production ML pipeline.

### Planned Dashboard Features

- Current AQI
- Predicted Next-Day AQI
- AQI Category
- PM2.5
- PM10
- Ozone
- Nitrogen Dioxide
- Live Air Quality Information
- Historical AQI Trends
- AQI Charts and Visualizations
- Model Prediction Information

### Dashboard Architecture

```text
User
 │
 ▼
Interactive Dashboard
 │
 ▼
FastAPI Backend
 │
 ▼
Prediction Service
 │
 ▼
Feast Feature Store
 │
 ▼
Random Forest Model
```

The dashboard will also be added to this repository and pushed to GitHub once completed.

---

# 🔮 Future Improvements

The project will continue to evolve with additional production features.

## Planned Features

### 🚀 Cloud Deployment

The complete system will be deployed to a cloud platform.

Future deployment architecture:

```text
Cloud Platform
     │
     ├── Interactive Dashboard
     │
     ├── FastAPI Backend
     │
     ├── AQI Scheduler
     │
     └── Persistent Feature Storage
```

### 📈 Additional Improvements

- Model monitoring
- Prediction monitoring
- Data drift detection
- CI/CD pipeline
- Cloud deployment
- Improved dashboard
- More ML models
- Model comparison
- Automated retraining
- Real-time AQI visualization

---

# 🎯 Key Production Concepts Demonstrated

This project demonstrates important Machine Learning Engineering concepts:

- Machine Learning Model Training
- Feature Engineering
- Live Data Integration
- Feature Store
- Model Serving
- REST APIs
- FastAPI
- Pydantic Validation
- Health Checks
- Readiness Checks
- Logging
- Error Handling
- Automated Scheduling
- Docker
- Docker Compose
- Persistent Storage
- Environment Variables
- Automated Testing
- Git
- GitHub

---

# 👨‍💻 Author

**Mubashir Azeem Abbasi**

Computer Science Graduate  
AI & Machine Learning Enthusiast

GitHub: https://github.com/mubashir-azeem

---

# 📌 Project Status

| Component | Status |
|---|---|
| Machine Learning Model | ✅ Completed |
| Feature Engineering | ✅ Completed |
| Feast Feature Store | ✅ Integrated |
| Live Feature Pipeline | ✅ Completed |
| FastAPI API | ✅ Completed |
| Docker | ✅ Completed |
| Docker Compose | ✅ Completed |
| Automated Scheduler | ✅ Completed |
| Automated Testing | ✅ Completed |
| GitHub Repository | ✅ Completed |
| Interactive Dashboard | 🟡 Coming Next |
| Cloud Deployment | 🟡 Planned |
