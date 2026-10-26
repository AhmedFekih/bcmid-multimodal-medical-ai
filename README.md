# BCMID — Multimodal Breast Cancer AI with Explainability

Academic project combining mammography and ultrasound processing, explainable computer vision, retrieval-augmented generation and multi-agent orchestration.

**Original team repository:** [mohamedmalekh/bcmid-multimodal-medical-ai](https://github.com/mohamedmalekh/bcmid-multimodal-medical-ai).

## Pipeline

```text
Mammography + ultrasound
    -> data quality / preprocessing
    -> dual-branch ResNet18 and feature fusion
    -> Grad-CAM explanations
    -> clinical retrieval and structured reporting
    -> safety checks / n8n orchestration
```

## Ahmed Fekih's contribution

The original team README identifies Ahmed Fekih as **Computer Vision & Explainable AI (XAI) Lead**, covering the multimodal dual-branch ResNet18 architecture, feature fusion and Grad-CAM activation maps.

## Team attribution

- **Ahmed Fekih:** computer vision and explainable AI.
- **Ikbel Hamdi:** clinical RAG and medical reporting.
- **Mohamed Malek Hammami:** agentic architecture, backend and integration.
- **Samar Omrani:** data engineering and safety verification.

The original detailed team documentation is preserved in [README.upstream.md](README.upstream.md).

## Repository guide

| Path | Purpose |
| --- | --- |
| `api_server.py` | FastAPI server |
| `src/` | Core application modules |
| `dq_agent/` | Data-quality and preprocessing modules |
| `clinical_pipeline/` | Clinical retrieval, safety and reporting modules |
| `n8n_bcmid_workflow.json` | Orchestration workflow |
| `tests/` | Existing tests |
| `demo.mp4` | Recorded demonstration |
| `BCMID_Rapport_Technique_FR.md` | French technical report |
| `BCMID_Final_Technical_Report_EN.md` | English technical report |

## Local setup

Create a Python virtual environment, then start with `python -m pip install -r requirements.txt`.

**Dependency limitation:** the root requirements file does not list every package imported by the API and model modules. The selected execution path also requires packages such as PyTorch/torchvision, FastAPI/Uvicorn, Transformers, sentence-transformers and ReportLab. Choose compatible versions for the machine and model checkpoints before running `python api_server.py`.

Use `.env.example` and `config.yaml` to configure a local environment. Model checkpoints and datasets must be available at the expected locations. The existing test command is `python -m pytest tests -v`; it was not run during this README update.

## Scope

A research and educational prototype. This portfolio description makes no claim of clinical validation, regulatory approval or production readiness. Existing reports remain available for reviewing the project's experiments and assumptions.
