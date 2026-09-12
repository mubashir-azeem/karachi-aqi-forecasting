# 🌍 Karachi AQI Forecasting System

<div align="center">

### AI-Powered Air Quality Prediction & Monitoring System for Karachi

Machine Learning • Feature Store • Explainable AI • API • Docker • AWS

<br>

🌐 **Live Application:** http://ec2-98-81-175-190.compute-1.amazonaws.com/

📊 **API Documentation:** http://ec2-98-81-175-190.compute-1.amazonaws.com/docs

</div>

---

# 📌 Project Overview

The **Karachi AQI Forecasting System** is an end-to-end Machine Learning application designed to predict the **next day's Air Quality Index (AQI) for Karachi, Pakistan**.

The system combines:

- Historical air quality data
- Live air quality data
- Feature engineering
- Machine Learning
- Feast Feature Store
- SHAP Explainable AI
- FastAPI
- Streamlit
- Docker
- Automated scheduling
- AWS EC2 deployment

The application automatically retrieves the latest air quality data, creates model features, stores them in the **Feast Feature Store**, and generates AQI predictions using a trained **Random Forest model**.

The system also provides explanations for predictions using **SHAP values**, helping users understand which features influenced the predicted AQI.

---

# 🎯 Project Objectives

The main objectives of this project are:

- Predict the next day's AQI for Karachi
- Use live air quality data
- Automate feature updates
- Store features using Feast Feature Store
- Build a Machine Learning prediction API
- Explain predictions using SHAP
- Provide an interactive Streamlit dashboard
- Containerize the complete application using Docker
- Deploy the system on AWS EC2
- Build a production-style Machine Learning pipeline

---

# 🚀 Live Deployment

The application is deployed on **AWS EC2**.

## 🌐 Live Application

http://ec2-98-81-175-190.compute-1.amazonaws.com/

## 📊 API Documentation

http://ec2-98-81-175-190.compute-1.amazonaws.com/docs

## 🔮 Prediction API

http://ec2-98-81-175-190.compute-1.amazonaws.com/predict

## 🧠 Explainability API

http://ec2-98-81-175-190.compute-1.amazonaws.com/explain

---

# ✨ Key Features

## 🤖 Machine Learning Prediction

The system uses a trained **Random Forest Regression model** to predict the next day's AQI.

Example prediction:

```json
{
  "city": "Karachi",
  "predicted_aqi": 70.91,
  "aqi_category": "Moderate",
  "prediction_for": "next day",
  "model": "Random Forest",
  "feature_store": "Feast"
}
```

---

## 📡 Live Air Quality Data

The system retrieves the latest live air quality information.

The live data includes features such as:

- PM2.5
- PM10
- Carbon Monoxide
- Nitrogen Dioxide
- Sulphur Dioxide
- Ozone
- Dust
- UV Index
- Aerosol Optical Depth
- US AQI
- European AQI

---

## ⚙️ Automated Feature Pipeline

A scheduler automatically runs the live feature update pipeline.

The current update interval is:

```text
Every 6 Hours
```

The scheduler performs the following tasks:

1. Fetch latest live air quality data
2. Convert hourly data into daily averages
3. Load historical air quality data
4. Combine historical and live data
5. Create model features
6. Generate lag features
7. Generate rolling features
8. Prepare the latest feature record
9. Push features to Feast Online Store

---

## 🏪 Feast Feature Store

The project uses **Feast** as the Feature Store.

Feast is responsible for storing and serving the latest Machine Learning features.

The system uses:

- Offline Feature Source
- Push Source
- Online Feature Store
- Feature View
- Feature Service

The API retrieves the latest features directly from the Feast Online Store before making a prediction.

---

## 🧠 SHAP Explainable AI

The project uses **SHAP** to explain Machine Learning predictions.

SHAP helps identify:

- Which features increased the AQI prediction
- Which features decreased the AQI prediction
- The importance of individual features

Example explanation:

```json
{
  "feature": "pm2_5",
  "feature_value": 20.2042,
  "shap_value": -20.2675,
  "impact": "decreases AQI"
}
```

Example API response:

```json
{
  "city": "Karachi",
  "model": "Random Forest",
  "explanation": [
    {
      "feature": "pm2_5",
      "feature_value": 20.2042,
      "shap_value": -20.2675,
      "impact": "decreases AQI"
    },
    {
      "feature": "european_aqi",
      "feature_value": 45.125,
      "shap_value": 1.6614,
      "impact": "increases AQI"
    }
  ]
}
```

---

## 📊 Interactive Dashboard

The project includes a **Streamlit dashboard**.

The dashboard allows users to:

- View predicted AQI
- View AQI category
- View prediction information
- View model information
- View feature explanations
- Interact with the AQI forecasting system

---

## 🔌 REST API

The project provides a REST API using **FastAPI**.

Available endpoints include:

| Endpoint | Description |
|---|---|
| `/` | Application information |
| `/health` | Health check |
| `/predict` | Generate AQI prediction |
| `/explain` | Get SHAP explanation |
| `/docs` | Interactive API documentation |

---

# 🏗️ System Architecture

```text
                    ┌───────────────────────┐
                    │   Live AQI Data API   │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ update_live_features │
                    │       Pipeline       │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Historical AQI Data   │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Feature Engineering   │
                    │                       │
                    │ • Date Features       │
                    │ • Lag Features        │
                    │ • Rolling Features    │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Feast Feature Store │
                    │                       │
                    │ • Feature View        │
                    │ • Push Source         │
                    │ • Online Store        │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │      FastAPI API      │
                    │                       │
                    │ GET /predict          │
                    │ GET /explain          │
                    └───────────┬───────────┘
                                │
                  ┌─────────────┴─────────────┐
                  ▼                           ▼
       ┌────────────────────┐      ┌────────────────────┐
       │ Random Forest Model│      │   SHAP Explainer   │
       └─────────┬──────────┘      └─────────┬──────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               │
                               ▼
                    ┌───────────────────────┐
                    │ Streamlit Dashboard   │
                    └───────────────────────┘
```

---

# 🔄 Complete Machine Learning Workflow

```text
Historical Data
      +
Live AQI Data
      │
      ▼
Data Processing
      │
      ▼
Feature Engineering
      │
      ▼
21 Model Features
      │
      ▼
Feast Feature Store
      │
      ▼
FastAPI
      │
      ├──────────────► Random Forest Prediction
      │
      └──────────────► SHAP Explanation
                               │
                               ▼
                       Streamlit Dashboard
                               │
                               ▼
                         AWS Deployment
```

---

# 📊 Dataset Information

The project uses air quality data for Karachi.

The historical dataset contains information such as:

- PM2.5
- PM10
- Carbon Monoxide
- Nitrogen Dioxide
- Sulphur Dioxide
- Ozone
- Dust
- UV Index
- Aerosol Optical Depth
- US AQI
- European AQI

Historical data is combined with the latest live air quality data to generate updated features.

---

# ⚙️ Feature Engineering

The model uses **21 features**.

## 🌫️ Air Pollution Features

```text
pm10
pm2_5
carbon_monoxide
nitrogen_dioxide
sulphur_dioxide
ozone
aerosol_optical_depth
dust
uv_index
```

---

## 📊 AQI Features

```text
us_aqi
european_aqi
```

---

## 📅 Date Features

```text
year
month
day
day_of_week
```

---

## ⏮️ Lag Features

Lag features use previous AQI values.

```text
us_aqi_lag_1
us_aqi_lag_3
us_aqi_lag_7
```

These represent AQI values from previous days.

---

## 📈 Rolling Features

Rolling features capture AQI trends.

```text
us_aqi_roll_3
us_aqi_roll_7
us_aqi_roll_std_7
```

These features help the model understand recent AQI patterns.

---

# 🤖 Machine Learning Model

The project uses:

## Random Forest Regressor

Random Forest is an ensemble Machine Learning algorithm.

It creates multiple decision trees and combines their predictions.

### Why Random Forest?

- Works well with structured data
- Handles non-linear relationships
- Captures complex feature interactions
- Provides strong prediction performance
- Provides feature importance
- Works well with AQI prediction features

---

# 📈 Model Performance

The trained model achieved the following results:

| Metric | Result |
|---|---:|
| MAE | 7.36 |
| RMSE | 10.31 |
| R² Score | 0.8109 |

The Random Forest model performed significantly better than the baseline model.

---

# 📊 Baseline vs Random Forest

| Model | MAE | RMSE |
|---|---:|---:|
| Baseline | 11.87 | 16.67 |
| Random Forest | 7.36 | 10.31 |

---

# 🏪 Feast Feature Store

The project uses **Feast** to manage Machine Learning features.

## Feast Components

### Entity

```text
city
```

Example:

```text
Karachi
```

---

### Feature View

```text
karachi_aqi_features
```

The Feature View contains all 21 Machine Learning features.

---

### Push Source

```text
karachi_aqi_push_source
```

The scheduler pushes the latest features into Feast.

---

### Feature Service

```text
karachi_aqi_prediction_service
```

The Feature Service groups the features required for prediction.

---

## Feature Retrieval Flow

```text
Live Data
    │
    ▼
Feature Engineering
    │
    ▼
Push to Feast
    │
    ▼
Feast Online Store
    │
    ▼
FastAPI retrieves features
    │
    ▼
Random Forest Prediction
```

---

# 🔮 Prediction Pipeline

When a user calls:

```text
/predict
```

The following process happens:

```text
Request
   │
   ▼
FastAPI
   │
   ▼
Retrieve Latest Features
from Feast
   │
   ▼
Ensure Feature Order
   │
   ▼
Random Forest Model
   │
   ▼
Predicted AQI
   │
   ▼
AQI Category
   │
   ▼
JSON Response
```

---

# 🧠 Explainability Pipeline

When a user calls:

```text
/explain
```

The following process happens:

```text
Request
   │
   ▼
FastAPI
   │
   ▼
Retrieve Latest Features
from Feast
   │
   ▼
SHAP Tree Explainer
   │
   ▼
Calculate SHAP Values
   │
   ▼
Sort Important Features
   │
   ▼
Return Explanation
```

---

# 📊 AQI Categories

The predicted AQI is converted into an AQI category.

Categories include:

| AQI Category |
|---|
| Good |
| Moderate |
| Unhealthy for Sensitive Groups |
| Unhealthy |
| Very Unhealthy |
| Hazardous |

Example:

```text
Predicted AQI: 70.91

Category: Moderate
```

---

# 🔌 API Endpoints

## 🏠 Root Endpoint

### Request

```bash
curl http://localhost:8000/
```

---

## ❤️ Health Check

### Request

```bash
curl http://localhost:8000/health
```

This endpoint checks whether the API is running correctly.

---

## 🔮 Predict AQI

### Request

```bash
curl http://localhost:8000/predict
```

### Example Response

```json
{
  "city": "Karachi",
  "predicted_aqi": 70.91,
  "aqi_category": "Moderate",
  "prediction_for": "next day",
  "model": "Random Forest",
  "feature_store": "Feast",
  "timestamp": "2026-09-12T05:52:09.661962"
}
```

---

## 🧠 Explain Prediction

### Request

```bash
curl http://localhost:8000/explain
```

### Example Response

```json
{
  "city": "Karachi",
  "model": "Random Forest",
  "explanation": [
    {
      "feature": "pm2_5",
      "feature_value": 20.2042,
      "shap_value": -20.2675,
      "impact": "decreases AQI"
    },
    {
      "feature": "european_aqi",
      "feature_value": 45.125,
      "shap_value": 1.6614,
      "impact": "increases AQI"
    },
    {
      "feature": "ozone",
      "feature_value": 48.2917,
      "shap_value": -0.9532,
      "impact": "decreases AQI"
    }
  ]
}
```

---

# 📚 API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://localhost:8000/docs
```

For the deployed application:

```text
http://ec2-98-81-175-190.compute-1.amazonaws.com/docs
```

---

# 🐳 Docker Architecture

The project uses Docker Compose to run multiple services.

```text
                    Docker Compose
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
       FastAPI        Streamlit       Scheduler
          │               │               │
          ▼               ▼               ▼
       API Service     Dashboard      Auto Updates
          │                               │
          └───────────────┬───────────────┘
                          │
                          ▼
                    Feast Store
                          │
                          ▼
                   Random Forest
```

---

# 🐳 Docker Services

The application contains the following services.

## API Service

```text
Service: api
Technology: FastAPI
Port: 8000
```

Responsibilities:

- Serve prediction API
- Retrieve features from Feast
- Load Random Forest model
- Generate predictions
- Generate SHAP explanations

---

## Frontend Service

```text
Service: frontend
Technology: Streamlit
Port: 8501
```

Responsibilities:

- Display application interface
- Display predictions
- Display AQI information
- Interact with the API

---

## Scheduler Service

```text
Service: scheduler
Technology: Python
```

Responsibilities:

- Automatically update live features
- Fetch latest air quality data
- Create features
- Push features to Feast

Current schedule:

```text
Every 6 Hours
```

---

# 📁 Project Structure

```text
karachi-aqi-forecasting
│
├── app
│   ├── __init__.py
│   └── main.py
│
├── src
│   ├── config.py
│   ├── feature_engineering.py
│   ├── prediction_service.py
│   ├── scheduler.py
│   └── update_live_features.py
│
├── frontend
│   └── app.py
│
├── feature_repo
│   │
│   ├── feature_repo
│   │   ├── data
│   │   ├── feature_definitions.py
│   │   └── feature_store.yaml
│   │
│   └── .gitignore
│
├── data
│   └── raw
│       └── air_quality
│           └── air_quality_historical.csv
│
├── models
│   └── aqi_random_forest.joblib
│
├── notebooks
│
├── Dockerfile
├── Dockerfile.frontend
├── Dockerfile.scheduler
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🛠️ Technologies Used

## Programming Language

- Python

---

## Machine Learning

- Scikit-learn
- Random Forest Regressor
- Joblib

---

## Data Processing

- Pandas
- NumPy

---

## Feature Store

- Feast

---

## Explainable AI

- SHAP

---

## Backend

- FastAPI
- Uvicorn

---

## Frontend

- Streamlit

---

## API Communication

- Requests
- REST API

---

## Containerization

- Docker
- Docker Compose

---

## Cloud Deployment

- AWS EC2

---

## Version Control

- Git
- GitHub

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/mubashir-azeem/karachi-aqi-forecasting.git
```

---

## 2. Open Project

```bash
cd karachi-aqi-forecasting
```

---

## 3. Create Environment File

Create:

```text
.env
```

Example:

```env
CITY=Karachi

SCHEDULER_INTERVAL_HOURS=6
```

The `.env` file should not be pushed to GitHub.

---

## 4. Build Docker Containers

```bash
docker compose build
```

---

## 5. Start Application

```bash
docker compose up -d
```

---

## 6. Check Running Containers

```bash
docker compose ps
```

Example services:

```text
karachi-aqi-api
karachi-aqi-frontend
karachi-aqi-scheduler
```

---

# 🧪 Testing the Application

## Test Prediction

```bash
curl http://localhost:8000/predict
```

---

## Test SHAP Explanation

```bash
curl http://localhost:8000/explain
```

---

## Check API Health

```bash
curl http://localhost:8000/health
```

---

# 🔄 Update Live Features Manually

The scheduler automatically updates features every 6 hours.

You can also manually run the pipeline.

```bash
docker compose exec scheduler python src/update_live_features.py
```

The pipeline performs:

```text
Fetch Live Data
      ↓
Convert Hourly Data
      ↓
Create Daily Data
      ↓
Load Historical Data
      ↓
Combine Data
      ↓
Create Features
      ↓
Prepare Latest Record
      ↓
Push to Feast
```

---

# 🏪 Check Feast Features

The latest features are stored inside the Feast Online Store.

The API retrieves the latest feature values before prediction.

Example feature retrieval process:

```text
Feast Online Store
        ↓
get_latest_features()
        ↓
21 Model Features
        ↓
Random Forest Model
        ↓
AQI Prediction
```

---

# ⏰ Scheduler

The scheduler starts automatically when the Docker container starts.

The scheduler:

```text
START
  │
  ▼
Update Features Immediately
  │
  ▼
Wait 6 Hours
  │
  ▼
Update Features Again
  │
  ▼
Repeat Forever
```

The scheduler script is located at:

```text
src/scheduler.py
```

---

# 📜 Scheduler Logs

Check scheduler logs:

```bash
docker compose logs scheduler
```

Check recent logs:

```bash
docker compose logs scheduler --tail=100
```

Example successful output:

```text
KARACHI AQI FEATURE SCHEDULER STARTED

RUNNING AUTOMATIC FEATURE UPDATE

Fetching latest live air quality data...

Live API request successful!

Creating 21 model features...

Pushing latest features to Feast Online Store...

LIVE FEATURES PUSHED TO FEAST SUCCESSFULLY!

PIPELINE COMPLETED SUCCESSFULLY!

FEATURE UPDATE COMPLETED SUCCESSFULLY
```

---

# 🔄 Restart Scheduler

If required:

```bash
docker compose restart scheduler
```

Check logs:

```bash
docker compose logs scheduler --tail=100
```

---

# 🛑 Stop Application

Stop all containers:

```bash
docker compose down
```

---

# ▶️ Start Application Again

```bash
docker compose up -d
```

---

# 🔁 Restart All Services

```bash
docker compose restart
```

---

# 🧹 Rebuild Application

If Docker code or dependencies are updated:

```bash
docker compose down
```

Then:

```bash
docker compose build
```

Then:

```bash
docker compose up -d
```

---

# ☁️ AWS EC2 Deployment

The application is deployed on an AWS EC2 instance.

The EC2 instance runs:

- FastAPI
- Streamlit
- Scheduler
- Feast Feature Store
- Random Forest Model
- SHAP Explainer
- Docker Containers

---

# 🌐 AWS Public URL

The application can be accessed using the EC2 Public DNS:

```text
http://ec2-98-81-175-190.compute-1.amazonaws.com/
```

The application can also be accessed using the EC2 Public IP:

```text
http://98.81.175.190/
```

---

# 🐳 Deployment Commands

Connect to the EC2 instance.

Navigate to the project:

```bash
cd ~/karachi-aqi-forecasting
```

Check containers:

```bash
docker compose ps
```

Check logs:

```bash
docker compose logs
```

Start containers:

```bash
docker compose up -d
```

Stop containers:

```bash
docker compose down
```

Restart containers:

```bash
docker compose restart
```

---

# 🔄 Updating the Deployed Application

When code is updated locally and pushed to GitHub:

```bash
git add .
```

```bash
git commit -m "Update application"
```

```bash
git push origin main
```

Then connect to AWS EC2.

Go to the project:

```bash
cd ~/karachi-aqi-forecasting
```

Pull the latest code:

```bash
git pull origin main
```

Rebuild containers:

```bash
docker compose build
```

Start updated containers:

```bash
docker compose up -d
```

Check status:

```bash
docker compose ps
```

---

# 🔐 Environment Variables

Sensitive configuration values should be stored inside:

```text
.env
```

Example:

```env
CITY=Karachi

SCHEDULER_INTERVAL_HOURS=6
```

The `.env` file should not be pushed to GitHub.

---

# 🛡️ Git Ignore Configuration

The project ignores:

```text
.env

__pycache__/

*.log

*.db

*.sqlite

*.sqlite3

feature_repo/feature_repo/data/

venv/

.venv/

.vscode/

.idea/
```

This prevents unnecessary and sensitive files from being pushed to GitHub.

---

# 📊 Current Application Status

## Machine Learning Model

```text
Status: Working
Model: Random Forest
```

---

## Feature Store

```text
Status: Working
Technology: Feast
```

---

## Live Feature Pipeline

```text
Status: Working
```

---

## Scheduler

```text
Status: Working

Update Interval:
Every 6 Hours
```

---

## Prediction API

```text
Status: Working

Endpoint:
/predict
```

---

## Explainability API

```text
Status: Working

Endpoint:
/explain
```

---

## Docker Deployment

```text
Status: Working
```

---

## AWS Deployment

```text
Status: Working
```

---

# 📸 Application Screenshots

Add your project screenshots inside a folder:

```text
assets/screenshots/
```

Recommended structure:

```text
assets
└── screenshots
    ├── dashboard.png
    ├── prediction.png
    ├── explanation.png
    ├── api-docs.png
    ├── docker-services.png
    └── scheduler.png
```

Then display them in the README.

## Dashboard

```markdown
![Dashboard](assets/screenshots/dashboard.png)
```

## Prediction

```markdown
![Prediction](assets/screenshots/prediction.png)
```

## SHAP Explanation

```markdown
![Explanation](assets/screenshots/explanation.png)
```

## API Documentation

```markdown
![API Documentation](assets/screenshots/api-docs.png)
```

## Docker Services

```markdown
![Docker Services](assets/screenshots/docker-services.png)
```

## Scheduler

```markdown
![Scheduler](assets/screenshots/scheduler.png)
```

---

# 🧠 Example SHAP Insights

Example explanation generated by the system:

| Feature | Impact |
|---|---|
| PM2.5 | Decreases AQI |
| European AQI | Increases AQI |
| Ozone | Decreases AQI |
| Sulphur Dioxide | Decreases AQI |
| US AQI | Increases AQI |
| UV Index | Increases AQI |
| Nitrogen Dioxide | Increases AQI |
| 7-Day AQI Rolling Average | Decreases AQI |

These explanations help understand why the Machine Learning model generated a particular AQI prediction.

---

# 🔍 Example Live Feature Record

The latest feature pipeline generates a record similar to:

```text
City: Karachi

PM10: 38.120833

PM2.5: 20.204167

Carbon Monoxide: 265.25

Nitrogen Dioxide: 18.65

Sulphur Dioxide: 8.420833

Ozone: 48.291667

Dust: 28.083333

UV Index: 2.270833

US AQI: 74.625

European AQI: 45.125

Year: 2026

Month: 9

Day: 12

Day of Week: 5
```

Additional lag and rolling features are also generated before pushing the record to Feast.

---

# 🎓 What This Project Demonstrates

This project demonstrates knowledge of:

## Machine Learning

- Regression
- Random Forest
- Model Evaluation
- Feature Engineering
- AQI Prediction

## Feature Engineering

- Lag Features
- Rolling Features
- Date Features
- Data Combination
- Live Data Processing

## MLOps

- Feature Store
- Feast
- Online Features
- Automated Feature Updates
- Scheduled Pipelines

## Explainable AI

- SHAP
- Feature Contribution
- Model Interpretation

## Backend Development

- FastAPI
- REST APIs
- API Documentation
- JSON Responses

## Frontend Development

- Streamlit
- Interactive Dashboard

## DevOps

- Docker
- Docker Compose
- Multi-container Applications

## Cloud

- AWS EC2
- Linux
- Remote Deployment

## Version Control

- Git
- GitHub

---

# 🚀 Future Improvements

Possible future improvements include:

- Add model monitoring
- Add data drift detection
- Add prediction monitoring
- Add experiment tracking using MLflow
- Add CI/CD pipeline using GitHub Actions
- Add automated model retraining
- Add PostgreSQL Feature Store
- Add Redis Online Store
- Add Prometheus monitoring
- Add Grafana dashboards
- Add Nginx reverse proxy
- Add HTTPS with SSL
- Add custom domain
- Add historical AQI visualizations
- Add multiple city support
- Add weather forecasting features
- Add deep learning models
- Compare multiple Machine Learning models
- Add model registry
- Add automated alerts

---

# 🧰 Useful Commands

## Check Containers

```bash
docker compose ps
```

---

## Start Containers

```bash
docker compose up -d
```

---

## Stop Containers

```bash
docker compose down
```

---

## Restart Containers

```bash
docker compose restart
```

---

## Check API Logs

```bash
docker compose logs api
```

---

## Check Frontend Logs

```bash
docker compose logs frontend
```

---

## Check Scheduler Logs

```bash
docker compose logs scheduler
```

---

## Follow Scheduler Logs

```bash
docker compose logs -f scheduler
```

---

## Run Feature Pipeline Manually

```bash
docker compose exec scheduler python src/update_live_features.py
```

---

## Test Prediction

```bash
curl http://localhost:8000/predict
```

---

## Test Explanation

```bash
curl http://localhost:8000/explain
```

---

# 👨‍💻 Author

**Mubashir Azeem Abbasi**

Computer Science Graduate  
Artificial Intelligence & Machine Learning

GitHub:

https://github.com/mubashir-azeem

Project Repository:

https://github.com/mubashir-azeem/karachi-aqi-forecasting

---

# ⭐ Project Summary

The **Karachi AQI Forecasting System** is an end-to-end Machine Learning and MLOps project that predicts the next day's Air Quality Index for Karachi.

The complete system includes:

```text
Historical Data
      +
Live AQI Data
      ↓
Feature Engineering
      ↓
21 Model Features
      ↓
Feast Feature Store
      ↓
Random Forest Model
      ↓
AQI Prediction
      +
SHAP Explanation
      ↓
FastAPI
      ↓
Streamlit Dashboard
      ↓
Docker
      ↓
AWS EC2 Deployment
```

This project demonstrates how Machine Learning models can be transformed from a notebook-based model into a complete deployed application with:

- Live data
- Automated pipelines
- Feature Store
- Prediction API
- Explainable AI
- Interactive dashboard
- Docker containers
- Cloud deployment

---

<div align="center">

### ⭐ If you found this project interesting, consider giving the repository a star!

Built with ❤️ using Python, Machine Learning, Feast, FastAPI, Streamlit, Docker and AWS

</div>
