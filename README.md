# 🩺 BCMID: Multimodal Breast Cancer AI Diagnosis & Orchestration System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg?logo=pytorch)](https://pytorch.org)
[![n8n](https://img.shields.io/badge/n8n-Orchestration-FF6D5A.svg?logo=n8n)](https://n8n.io)
[![License](https://img.shields.io/badge/Academic-ESPRIT_Engineering-blue.svg)](https://esprit.tn)

> **ESPRIT 5th-Year Engineering Final Project (PFE)**  
> **Topic:** Multimodal Medical AI Automation System with Explainable AI (XAI), Clinical RAG, LLM Reasoning, and Hospital Workflow Orchestration for Breast Cancer Triage.

---

## 📌 Executive Summary

The **BCMID (Breast Cancer Multimodal Imaging Dataset) AI System** is an end-to-end clinical decision support platform designed to assist radiologists and hospital tumor boards in early breast cancer detection, risk stratification, and patient triage.

By unifying **Mammography** (tissue architecture & microcalcifications) and **Ultrasound** (morphology & acoustic attenuation) into a multimodal dual-branch convolutional neural network (**ResNet-18**), combined with an explainable AI (**Grad-CAM**) layer, an **ACR BI-RADS Retrieval-Augmented Generation (RAG)** engine, a **LLM Clinical Reasoning Agent**, and an automated **n8n hospital triage orchestrator**, the system achieves rigorous, reproducible, and explainable medical assessments.

```
                              BCMID END-TO-END PIPELINE ARCHITECTURE
                              
   [ Patient Ingestion ] ──────► [ Block 1: Data & Quality Agent ]
  (Mammography + Ultrasound)        ├── SHA-256 Patient Pseudonymization (Zero Leakage)
                                    ├── CLAHE Enhancement & Median Filtering (512×512)
                                    └── Integrity & Resolution Verification
                                                │
                                                ▼
                                 [ Block 2-3: Multimodal Vision CNN ]
                                    ├── Dual-Branch ResNet-18 Feature Extraction
                                    ├── Fusion Layer & BI-RADS Categorization
                                    └── Grad-CAM XAI Heatmap Generation
                                                │
                                                ▼
                                 [ Block 4: Clinical RAG Engine ]
                                    ├── ACR BI-RADS 5th Edition Guidelines Retrieval
                                    └── FAISS Vector Similarity & Evidence Grounding
                                                │
                                                ▼
                                 [ Block 5-6: Reasoning & Safety Agents ]
                                    ├── LLM Clinical Synthesis (Qwen2.5-3B)
                                    ├── Anti-Hallucination & Rule Verification (10 Tests)
                                    └── Human-in-the-Loop Validation Mandate
                                                │
                                                ▼
                                 [ Block 7: Box 7 Medical Report ]
                                    ├── Interactive HTML Clinical Report
                                    └── Structured JSON Medical Record
                                                │
                                                ▼
                                 [ Block 8: n8n Workflow Orchestration ]
                                    ├── URGENT     ➔ High-Priority Biopsy Alert + Committee Referral
                                    ├── SURV       ➔ 6-Month Short-Interval Follow-Up Schedule
                                    └── ROUTINE    ➔ Annual Standard Screening Confirmation
                                                │
                                                ▼
                                 [ Clinical Email Notification ]
                                    └── Automated Delivery to Attending Radiologist / RIS
```

---

## 🚀 Key Features

1. **Multimodal Deep Learning:**
   * Dual-encoder convolutional architecture (ResNet-18) processing paired Mammography and Ultrasound scans.
   * Multi-class BI-RADS prediction (1, 2, 3, 4A, 4B, 4C, 5, 6).
2. **Explainable AI (Grad-CAM XAI):**
   * Real-time activation heatmaps identifying focal lesions in mammograms and tissue borders in sonograms.
   * Visual alignment between AI attention and radiologist findings.
3. **Evidence-Based Clinical RAG:**
   * Knowledge base indexed with the American College of Radiology (ACR) BI-RADS Atlas (5th edition).
   * Dense vector retrieval via FAISS for grounded medical recommendations.
4. **Safety & Anti-Hallucination Guardrails:**
   * Automated verification loop validating 10 critical clinical guardrails (modality isolation, device verification, entropy uncertainty checks).
   * Strict human-in-the-loop requirement: *"MANDATORY — Licensed Radiologist Signature Required"*.
5. **Hospital Workflow Orchestration (n8n):**
   * Standard 8-node enterprise pipeline deployed on n8n (`http://localhost:5678`).
   * Automated dispatching based on urgency: immediate biopsy alerts vs. routine scheduling.
6. **Clinical Web Console (`form.html`):**
   * Real-time ingestion console at `http://localhost:8000/form`.
   * Drag-and-drop image upload, interactive Grad-CAM preview, and one-click benchmark cases.
7. **Automated Medical Email Dispatch:**
   * Generates and dispatches complete Box 7 medical reports and Grad-CAM attachments via SMTP.
   * Full HTML preview and `.eml` archive for hospital RIS integration.

---

## 🗂️ Repository Structure

```
deeplearning5eme/
├── api_server.py                 # Core FastAPI Microservices API (8 Agent Endpoints + Triage)
├── n8n_bcmid_workflow.json       # Official 8-Node n8n Orchestrator Workflow
├── requirements.txt              # Production Dependencies
├── config.yaml                   # Global Pipeline Configuration
├── BCMID_annotations.tsv        # Clinical Metadata & Ground-Truth Labels
├── README.md                     # Engineering & Research Documentation
│
├── ikbelwork/                    # Modular Clinical Agents
│   ├── clinical_rag_enhancer.py  # Block 4: ACR BI-RADS Vector RAG Engine
│   ├── safety_agent.py           # Block 6: Quality / Safety Verification Agent
│   ├── medical_report_generator.py # Block 7: Box 7 Medical Report Generator
│   ├── run_orchestrator.py       # End-to-end pipeline runner
│   └── acr_birads_guidelines.json # Clinical Knowledge Base
│
├── dq_agent/                     # Block 1: Data & Quality Processing Agent
│   ├── anonymize.py              # Salted SHA-256 patient pseudonymization
│   ├── integrity.py              # Image corruption & duplicate detection
│   ├── preprocess.py             # CLAHE (Mammo) & Median filter (US)
│   └── splits.py                 # Patient-level stratified Train/Val/Test split
│
├── bcmid_work/                   # Working Storage & Knowledge Index
│   ├── reports/
│   │   ├── form.html             # Clinical Ingestion Web Console
│   │   └── medical_report_*.html # Generated Interactive Box 7 Reports
│   ├── manifest.csv              # Validated Dataset Manifest (332 Patients)
│   ├── splits.json               # Zero-Leakage Dataset Split (70/15/15)
│   ├── rag_chunks.csv            # Tokenized Clinical Guidelines
│   └── final_medical_reports.json# 20 Benchmark Patient Reports
│
├── sample_data/                  # Real Benchmark Cases from Test Set (Hold-out)
│   ├── 1_CAS_MALADE_URGENT_P1eb742860c/  # BI-RADS 5 Malignant Case
│   ├── 2_CAS_SURVEILLANCE_Pf9bea655cf/   # BI-RADS 3 Probably Benign Case
│   └── 3_CAS_ROUTINE_SAIN_Paacb1ec57b/   # BI-RADS 1 Negative Routine Case
│
├── docs/                         # Official ESPRIT Technical & Academic Documentation
│   ├── Rapport_Technique_Lab_Data_Quality.pdf
│   └── Rapport_Technique_Lab_RAG_Agent.pdf
│
├── scripts/                      # PDF Report Generation Scripts
│   ├── generate_dq_report_pdf.py
│   └── generate_rag_report_pdf.py
│
└── tests/                        # Comprehensive Unit & Integration Tests
    ├── test_anonymize.py
    ├── test_integrity.py
    ├── test_preprocess.py
    └── test_splits.py
```

---

## 📊 Dataset & Splitting Methodology

* **Total Patients:** 332 patients (948 Mammographies, 1,049 Ultrasounds).
* **Patient-Level Split (Zero Data Leakage):**
  * **Train Set (70%):** 228 patients
  * **Validation Set (15%):** 47 patients
  * **Test Set (15%):** 57 patients *(Hold-out, strictly unseen during training)*
* **Data Leakage Guarantee:** `leakage = 0` (images from the same patient never overlap across splits).

---

## ⚡ Quickstart Guide

### 1. Installation
```bash
git clone https://github.com/mohamedmalekh/bcmid-multimodal-medical-ai.git
cd bcmid-multimodal-medical-ai

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the FastAPI Microservices Server
```bash
python api_server.py
```
* **Interactive Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Clinical Ingestion Web Console:** [http://localhost:8000/form](http://localhost:8000/form)

### 3. Start & Import the n8n Workflow
1. Launch n8n:
   ```bash
   npx n8n
   ```
2. Open `http://localhost:5678`.
3. In the top right menu (`...`), click **Import from File** and select `n8n_bcmid_workflow.json`.
4. Click **Publish** to enable the live webhook router.

---

## 🧪 Benchmark Test Cases

| Case | Patient ID | True Diagnosis | Predicted BI-RADS | n8n Triage Priority | Recommended Action |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Malignant** | `P1eb742860c` | Malignant | **BI-RADS 5** (94% conf) | **`URGENT`** | Image-Guided Core Needle Biopsy (CNB) |
| **Surveillance** | `Pf9bea655cf` | Benign | **BI-RADS 3** (78% conf) | **`SURVEILLANCE`** | Short-Interval 6-Month Unilateral Follow-Up |
| **Normal** | `Paacb1ec57b` | Normal | **BI-RADS 1** (94% conf) | **`ROUTINE`** | Annual Standard Screening Mammography |

---

## 🛡️ Medical Disclaimer
This software is developed strictly for **academic and research purposes** as part of an engineering degree final project at ESPRIT. It is not certified for autonomous clinical diagnostic use. All medical outputs and triage recommendations must be reviewed and signed by a licensed radiologist.

---

## 👨‍💻 Author
* **Mohamed Malek Hammami**  
* 5th-Year Engineering Student in Computer Science / Deep Learning & Medical AI  
* **ESPRIT (École Supérieure Privée d'Ingénierie et de Technologies), Tunis, Tunisia**
