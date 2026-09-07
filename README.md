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
