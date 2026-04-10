---
title: Email Triage OpenEnv
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
short_description: Email triage environment using OpenEnv
---

# 📧 Email Triage OpenEnv

This project implements an OpenEnv-compatible environment for email classification and prioritization.

---

## 🚀 Features

* Classify emails as **important** or **spam**
* Assign **priority levels** (low, medium, high)
* Built using **FastAPI**
* Fully **Dockerized**
* Deployed on **Hugging Face Spaces**

---

## 📡 API Endpoints

### 🔹 Reset Environment

`POST /reset`

---

### 🔹 Take Action

`POST /step`

Example:

```
{
  "action": {
    "email_id": 1,
    "label": "important",
    "priority": "high"
  },
  "timeout_s": 30
}
```

---

### 🔹 Get Tasks

`GET /tasks`

---

### 🔹 Grade Performance

`POST /grader`

Example:

```
{
  "task_id": "easy",
  "processed": [1, 2, 3, 4, 5]
}
```

---

## 🌐 Live Demo

👉 https://shrashti21-email-triage-openenv.hf.space/docs

---

## 🐳 Run Locally (Docker)

```
docker build -t email-triage .
docker run -p 8000:8000 email-triage
```

---

## 📁 Project Structure

```
email_triage_env/
│
├── server/
│   ├── app.py
│   └── email_triage_env_environment.py
│
├── models.py
├── openenv.yaml
├── Dockerfile
├── baseline.py
└── README.md
```

---

## 🎯 Purpose

This environment is designed for:

* Reinforcement Learning agents
* Email classification workflows
* Testing agent decision-making

---

✨ Built as part of OpenEnv assessment
