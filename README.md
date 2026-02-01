# IBM TrustBuild

> **The only "Idea-to-Deployment" engine that builds with compliance baked in.**

[![IBM watsonx](https://img.shields.io/badge/Powered%20by-watsonx.ai-blue?style=flat-square&logo=ibm)](https://www.ibm.com/products/watsonx-ai)
[![Langflow](https://img.shields.io/badge/Orchestrated%20with-Langflow-darkblue?style=flat-square)](https://www.langflow.build/)
[![IBM Granite](https://img.shields.io/badge/Models-IBM%20Granite-navy?style=flat-square&logo=ibm)](https://www.ibm.com/granite)
[![IBM Cloud](https://img.shields.io/badge/Deploy%20on-IBM%20Cloud-lightblue?style=flat-square&logo=ibm)](https://cloud.ibm.com)

---

## 🏆 IBM Dev Day: AI Demystified — Hackathon Submission

**Theme:** From Idea to Deployment

**Team:** cornerbrooke

---

## 📌 The Problem

The biggest bottleneck in the enterprise isn't writing code — it's **approval**. Developers want to move fast, but security and compliance teams act as the "brakes" because AI-generated code can be risky or misaligned with cloud best practices. The gap between *idea* and *deployed, compliant product* costs teams weeks.

## 🚀 The Solution

**IBM TrustBuild** bridges this gap by combining a generative **Architect Agent** with a real-time **Governance Guardrail** into a single, end-to-end pipeline.

| For Developers | For the Enterprise |
|---|---|
| Automates architecture scaffolding and boilerplate using **IBM Granite** | Ensures every generated line of code passes a **Pre-flight Governance Audit** |
| Generates Dockerfiles, Terraform, and IBM SDK integrations in seconds | Enforces encryption, VPC isolation, and policy compliance automatically |
| One prompt → deployment-ready kit | Innovation and regulation live in the **same workflow** |

---

## 🧠 Architecture: The TrustBuild Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER PROMPT INPUT                             │
│        "Build a customer portal for sensitive health data"          │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 1: INTENT EXTRACTION          [granite-3-8b-instruct]        │
│  ─────────────────────────────────────────────────────────────────  │
│  • Parses natural language into structured requirements              │
│  • Identifies: stack needs, data sensitivity, scale requirements    │
│  • Output → requirements.json                                       │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 2: ARCHITECT NODE (The Builder)                              │
│  ─────────────────────────────────────────────────────────────────  │
│  • Maps requirements → IBM Cloud services                           │
│  • Selects: Code Engine, Cloudant, watsonx.ai, Container Registry   │
│  • Output → architecture_manifest.json                              │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 3: GOVERNANCE GUARDRAIL (The Judge)   ⚡ INNOVATION LAYER   │
│  ─────────────────────────────────────────────────────────────────  │
│  • Auditor Agent scans manifest against Policy Knowledge Base       │
│  • Checks: encryption, VPC isolation, HIPAA, public API usage       │
│  • ❌ FAIL → Auto-corrects architecture before code generation      │
│  • ✅ PASS → Approves for code synthesis                            │
│  • Output → governance_report.json                                  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 4: SECURE CODE SYNTHESIS          [granite-20b-code]         │
│  ─────────────────────────────────────────────────────────────────  │
│  • Generates Dockerfile, Terraform, app boilerplate                 │
│  • Pre-configured with IBM SDKs and security policies               │
│  • Output → Deployment Kit (downloadable)                           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Role |
|---|---|---|
| Reasoning Engine | **watsonx.ai** (Granite 3.0) | Powers all agent reasoning |
| Intent Parsing | **Granite-3-8b-instruct** | Decomposes prompts into requirements |
| Code Generation | **Granite-20b-code** | Generates Dockerfiles, Terraform, boilerplate |
| Orchestration | **Langflow** | Connects the 4-stage multi-agent pipeline |
| Governance | **watsonx.governance** (simulated) | Policy enforcement and audit logic |
| Deployment Target | **IBM Cloud** | Code Engine, Cloudant, Container Registry |
| Frontend | **React + TypeScript** | Dashboard UI with real-time pipeline visualization |
| Backend | **Python (FastAPI)** | API layer connecting frontend to watsonx |

---

## 📂 Repository Structure

```
ibm-trustbuild/
├── README.md                   # This file
├── docker-compose.yml          # Full-stack local deployment
├── .env.example                # Environment variable template
│
├── frontend/                   # React + TypeScript dashboard
│   ├── package.json
│   ├── tsconfig.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── index.tsx
│       ├── App.tsx             # Root app with routing
│       ├── components/
│       │   ├── Header.tsx      # Top nav with branding
│       │   ├── Pipeline.tsx    # 4-stage pipeline visualization
│       │   ├── PromptInput.tsx # User prompt entry
│       │   ├── GovernancePanel.tsx  # Guardrail status display
│       │   └── OutputKit.tsx   # Final deployment kit display
│       └── styles/
│           └── globals.css     # IBM Carbon-inspired theming
│
├── backend/                    # Python FastAPI API server
│   ├── requirements.txt
│   ├── main.py                 # FastAPI app entry point
│   ├── routes/
│   │   └── pipeline.py         # /api/run-pipeline endpoint
│   ├── agents/
│   │   ├── intent_agent.py     # Stage 1: Intent Extraction
│   │   ├── architect_agent.py  # Stage 2: Architecture Mapping
│   │   ├── governance_agent.py # Stage 3: Governance Guardrail
│   │   └── codegen_agent.py    # Stage 4: Secure Code Synthesis
│   ├── services/
│   │   ├── watsonx_client.py   # watsonx.ai API wrapper
│   │   └── policy_kb.py        # Governance Policy Knowledge Base
│   └── models/
│       └── schemas.py          # Pydantic request/response models
│
├── langflow/                   # Langflow pipeline export
│   └── trustbuild_pipeline.json # Importable Langflow flow definition
│
├── scripts/                    # Utility and deployment scripts
│   ├── setup.sh                # One-command local environment setup
│   └── deploy_ibm_cloud.sh     # IBM Cloud deployment script
│
├── docker/                     # Docker configurations
│   ├── Dockerfile.frontend     # Frontend container
│   └── Dockerfile.backend      # Backend container
│
└── docs/                       # Supporting documentation
    └── DEMO_SCRIPT.md          # 2-minute demo video script
```

---

## ⚡ Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- Docker & Docker Compose (optional, for full-stack)
- IBM Cloud account with watsonx.ai access
- watsonx.ai API Key and Project ID

### 1. Clone & Configure

```bash
git clone https://github.com/cornerbrooke/ibm-trustbuild.git
cd ibm-trustbuild

# Copy and edit the environment file
cp .env.example .env
# Edit .env with your IBM watsonx credentials
```

### 2. Run with Docker Compose (Recommended)

```bash
docker-compose up --build
```

- **Frontend:** [http://localhost:3000](http://localhost:3000)
- **Backend API:** [http://localhost:8000](http://localhost:8000)
- **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Run Locally (Without Docker)

```bash
# Terminal 1: Frontend
cd frontend
npm install
npm run dev

# Terminal 2: Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🎬 Demo

See [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md) for the full 2-minute recorded demo script.

**Live Demo Flow:**
1. Open the TrustBuild dashboard
2. Enter: *"Build a customer portal that uses AI to analyze sensitive health data"*
3. Watch the 4-stage pipeline execute in real time
4. Observe the Governance Guardrail flag and auto-correct a HIPAA compliance issue
5. Download the final Deployment Kit

---

## 📋 Judging Criteria Alignment

| Criteria | How TrustBuild Scores |
|---|---|
| **Completeness & Feasibility (5pts)** | Full 4-stage pipeline with working frontend, backend, and Langflow export. Real watsonx.ai integration via API. |
| **Creativity & Innovation (5pts)** | The Governance Guardrail with auto-correction is the differentiator. No other "code generator" enforces compliance before synthesis. |
| **Design & Usability (5pts)** | IBM Carbon-inspired UI with real-time pipeline status, animated stage transitions, and a one-click deployment kit download. |
| **Effectiveness & Efficiency (5pts)** | Directly addresses the hackathon theme. Reduces idea-to-deployment from days to 60 seconds. Scales to any enterprise policy rulebook. |

---

## 📄 License

This project was built for the **IBM Dev Day: AI Demystified Hackathon** (January 2026).

---

*Built with watsonx. Governed by design.*
