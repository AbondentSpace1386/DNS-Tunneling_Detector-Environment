# DNS Tunneling Detection Environment (OpenEnv)

## 🧠 Overview
This project implements a Reinforcement Learning environment for detecting DNS tunneling attacks using OpenEnv. The agent interacts with the environment and decides whether to allow, investigate, or block DNS queries.

---

## 🎯 Objective
Build an OpenEnv-compatible environment where an agent learns to detect malicious DNS activity using structured features.

---

## ⚙️ Action Space
Discrete actions:
- 0 → Allow
- 1 → Investigate
- 2 → Block

---

## 📊 Observation Space
Feature vector (size = 4):
- Domain Length
- Request Frequency
- Entropy
- Query Type (encoded)

---

## 🧩 Tasks

### 1. Easy Detection
- Clear separation between normal and malicious traffic

### 2. Mixed Traffic
- Combination of normal, suspicious, and tunneling data

### 3. Obfuscated Tunnel
- Hard dataset with stealthy tunneling patterns

---

## 🏆 Reward Design
- Correct action → high reward
- Partial detection → moderate reward
- Incorrect action → penalty

Rewards are normalized to range [0, 1].

---

## 🚀 API Endpoints

| Endpoint | Method | Description |
|--------|--------|------------|
| `/reset` | POST | Reset environment with task |
| `/step` | POST | Perform action |
| `/state` | GET | Get current state |

---

## 🧪 Setup

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload