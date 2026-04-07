---
title: Email Triage OpenEnv
emoji: 🏆
colorFrom: purple
colorTo: green
sdk: docker
pinned: false
license: mit
short_description: Email triage OpenEnv environment for AI agents
---

# 📧 Email Triage OpenEnv

This project implements an OpenEnv-compatible environment for email classification and prioritization.

## 🚀 Features

- Classify emails as **important** or **spam**
- Assign **priority levels** (low, medium, high)
- Built using **FastAPI**
- Fully **Dockerized**
- Deployed on **Hugging Face Spaces**

---

## 📡 API Endpoints

### 🔹 Reset Environment
`POST /reset`

### 🔹 Take Action
`POST /step`

Example:
```json
{
  "action": {
    "email_id": 1,
    "label": "important",
    "priority": "high"
  },
  "timeout_s": 30
}
```
### Get Tasks
`GET /tasks`

### Grade Performance
`POST /grader`

Example:
```json
{
  "processed": [1, 2, 3, 4, 5]
}

```

### Live Demo
# 👉 https://shrashti21-email-triage-openenv.hf.space/docs


### Run Locally (Docker)
```bash
docker build -t email-triage .
docker run -p 8000:8000 email-triage

```

### Project Structure
email_triage_env/
├── server/
├── models.py
├── openenv.yaml
├── Dockerfile
├── baseline.py

### Purpose
This environment is designed for:
- Reinforcement Learning agents
- Email classification tasks
- Testing agent decision-making

### ✨ Built as part of OpenEnv assessment



