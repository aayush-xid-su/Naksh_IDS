# Naksh IDS – AI-Powered Intrusion Detection System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-green.svg)
![SOC](https://img.shields.io/badge/SOC-Intrusion%20Detection-orange.svg)
![Cybersecurity](https://img.shields.io/badge/Cybersecurity-IDS%2FIPS-red.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Active%20Development-success.svg)

---

## 🔐 Project Overview

**Naksh IDS** is a real-time, machine-learning–powered Intrusion Detection System (IDS) designed with a **Security Operations Center (SOC)** mindset.

The system detects, classifies, correlates, and escalates cyber threats by combining:
- ML-based attack classification
- Confidence scoring
- Trend tracking across batches
- Threat correlation & escalation logic
---

## 🎯 Why This Project Exists

Traditional IDS systems:
- Produce excessive false positives
- Fail to correlate events across time
- Lack intelligent alert prioritization

This project solves that by:
- Tracking attack trends across batches
- Dynamically assigning severity
- Escalating threats only when risk accumulates
- Reducing alert fatigue for SOC analysts

---

## 🧠 How It Works

1. **Data Ingestion**
   - Network / event feature vectors are streamed in batches

2. **ML Prediction**
   - A trained Random Forest model predicts attack class
   - Outputs confidence score

3. **Trend Analysis**
   - Tracks confidence changes across batches
   - Detects rising, falling, or stable threats

4. **Threat Correlation**
   - Aggregates events
   - Calculates threat score
   - Determines escalation level

5. **Intelligent Alerting**
   - Low confidence ≠ ignored
   - Alerts only when risk accumulates logically

---

## 🏗️ Architecture (High-Level)

```text
Data Stream
    ↓
ML Classifier (Random Forest)
    ↓
Confidence Scoring
    ↓
Trend Tracking (Batch-wise)
    ↓
Threat Correlation Engine
    ↓
Severity & Alert Decision
    ↓
SOC Output (JSON)
```

## 🛠️ Technologies Used

- Language: Python 3.9+

- Machine Learning: Scikit-learn (Random Forest)

- Data Processing: Pandas, NumPy

- Model Persistence: Joblib

- Architecture: Modular SOC-style pipeline



## ▶️ How to Run

1. #### Install dependencies
```
pip install -r requirements.txt

```
2. #### Train the model
```
python train_rf_model.py
```

3. #### Run real-time IDS
```
python -m realtime.main
```


## 📊Example Output
``` json
{
  "events": [
    {
      "attack": "Brute Force",
      "confidence": 0.29,
      "trend": "stable",
      "alert": false,
      "severity": "low"
    }
  ],
  "correlated_threat": {
    "threat_score": 32,
    "escalation": "low"
  },
  "timestamp": "2026-01-09 23:09:48"
}
```

## 🚀 Use Cases

- SOC threat analysis simulation

- IDS research & experimentation

- Final year / capstone cybersecurity project

- Blue team detection engineering practice

## 🔮 Future Enhancements

- Deep Learning models (LSTM for sequence attacks)

- Dashboard (SOC UI)

- Threat intelligence feeds

- Malware & phishing classification

- Dockerized deployment

- SIEM integration


## 👩‍💻Contributing to Naksh IDS

Thank you for your interest in contributing to **Naksh IDS**!  
This project aims to simulate a real-world SOC-grade Intrusion Detection System, and contributions are welcome.

---

## 🧭 Ways to Contribute

You can contribute by:

- Fixing bugs or improving stability
- Enhancing detection logic or ML models
- Improving performance or scalability
- Adding documentation or examples
- Proposing new SOC features (SIEM, dashboard, threat intel, etc.)

---

## 🛠️ Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/cyber_ids_soc.git
   cd cyber_ids_soc
   ```
3. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🌱 Branching Strategy

- ```main``` → Stable production-ready code

- ```dev``` → Active development

- Feature branches:
  ``` 
  feature/<feature-name>
  fix/<bug-name>
  ```

## 📐 Coding Guidelines

- Follow PEP8 for Python

- Use meaningful variable & function names

- Keep functions modular and testable

- Avoid hardcoded paths

- Add inline comments for complex logic

## 🧪 Testing

Before submitting a PR:

- Ensure the model trains successfully

- Ensure python -m realtime.main runs without errors

- Validate JSON output format

## 📥 Pull Request Process

1. Push changes to your fork

2. Open a Pull Request against ```main```

3. Clearly describe:

    What was changed

    Why it was changed

    Any breaking changes

## 📌 Contribution Rules

- No malicious payloads

- No backdoors

- No plagiarism

- Respect the project’s purpose (defensive security)