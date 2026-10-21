# 🩺 BCMID: Breast Cancer Multimodal Intelligent Diagnosis & Hospital Triage System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg?logo=pytorch)](https://pytorch.org)
[![Tests Passing](https://img.shields.io/badge/pytest-61%2F61%20passing-brightgreen.svg?logo=pytest)](https://docs.pytest.org)
[![n8n](https://img.shields.io/badge/n8n-Orchestration-FF6D5A.svg?logo=n8n)](https://n8n.io)
[![Regulatory](https://img.shields.io/badge/Regulatory-SaMD_Class_IIa-blue.svg)](https://health.ec.europa.eu)
[![Institution](https://img.shields.io/badge/Academic-ESPRIT_Engineering-003366.svg)](https://esprit.tn)

> **Projet d'Ingénierie de 5\textsuperscript{ème} Année – Deep Learning & Intelligence Artificielle**  
> **Institution :** ESPRIT (École Supérieure Privée d'Ingénierie et de Technologies), Tunis, Tunisie  
> **Année Universitaire :** 2026 – 2027  
> **Thématique :** Système d'aide à la décision clinique multimodale (Mammographie plein champ + Échographie ciblée), explicabilité XAI (Grad-CAM), RAG clinique (Atlas ACR BI-RADS), raisonnement LLM sous garde-fous déterministes et orchestration hospitalière automatisée sous n8n.

---

## 👥 Équipe Projet & Encadrement Pédagogique

Ce travail d'ingénierie a été conçu, développé et évalué collectivement par les élèves-ingénieurs de la filière **Data Science, Deep Learning & Intelligence Artificielle (5\textsuperscript{ème} Année)** :

| Membre de l'Équipe | Rôle Principal & Contributions Clés |
| :--- | :--- |
| **Ikbel Hamdi** | **Clinical RAG & Medical Reporting Lead**<br>Indexation vectorielle FAISS de l'Atlas ACR BI-RADS 5\textsuperscript{e} édition, générateur de comptes-rendus cliniques structurés (Box 7) et pipeline clinique. |
| **Ahmed Fekih** | **Computer Vision & Explainable AI (XAI) Lead**<br>Architecture CNN multimodale à double branche ResNet-18, fusion des descripteurs radiologiques et génération des cartes d'activation Grad-CAM. |
| **Mohamed Malek Hammami** | **Agentic Architecture, Backend & Integration Lead**<br>Déploiement des microservices FastAPI, orchestrateur hospitalier n8n (8 nœuds), serveur de production et intégration des flux de triage. |
| **Samar Omrani** | **Data Engineering & Safety Verification Lead**<br>Prétraitement d'images (CLAHE, filtrage médian), split sans fuite patient (`leakage = 0`), agent de sécurité déterministe et tests adversariaux. |

### 🎓 Encadrement Académique
* **Mme Oumayma Guasmi** — *Enseignante-Chercheuse en Deep Learning & Intelligence Artificielle, ESPRIT*

---

## 📌 Résumé Exécutif / Executive Summary

Le cancer du sein est la première néoplasie féminine mondiale. Si le dépistage par **Mammographie Numérique Plein Champ (FFDM)** réduit la mortalité de 20% à 30%, son usage en modalité unique présente deux limitations majeures :
1. **Masquage parenchymateux en seins denses (ACR C/D) :** La sensibilité mammographique chute sous les 48% par superposition fibro-glandulaire.
2. **Surcharge de biopsies bénignes :** Plus de 70% des macro-biopsies percutanées se révèlent histologiquement bénignes, générant anxiété et surcoûts hospitaliers.

Le système **BCMID** (*Breast Cancer Multimodal Intelligent Diagnosis*) résout ces défis par la synergie binationale et bimodale de la **Mammographie** (détection des microcalcifications et distorsions) et de l'**Échographie ciblée** (insensible à la densité, caractérisation solide vs liquide).

BCMID articule une chaîne multi-agents modulaire conforme à la réglementation européenne **MDR 2017/745 (SaMD Classe IIa)**, intégrant un contrôle humain obligatoire (*Human-in-the-Loop*) sur chaque décision diagnostique.

---

## 🏗️ Architecture Globale du Système

```
                             FLUX CLINIQUE & ARCHITECTURE MULTI-AGENTS BCMID
                             
   [ Patient Cliché Ingestion ] ──────► [ Agent 1: Data & Quality Processing ]
  (Mammographie FFDM + Écho US)             ├── Pseudonymisation SHA-256 salée (Zéro fuite RGPD)
                                            ├── Rehaussement CLAHE (Mammo) & Filtrage médian (US)
                                            └── Validation d'intégrité & Résolution 512×512
                                                        │
                                                        ▼
                                         [ Agents 2-3: Vision Multimodale CNN ]
                                            ├── Encodeurs parallèles ResNet-18 (Mammo + US)
                                            ├── Fusion de caractéristiques (Concaténation + FC)
                                            ├── Prédiction catégorielle ACR BI-RADS (1 à 6)
                                            └── Cartes d'activation d'attention Grad-CAM
                                                        │
                                                        ▼
                                         [ Agent 4: Clinical RAG Engine ]
                                            ├── Base de connaissances : Atlas ACR BI-RADS (5e éd.)
                                            ├── Embeddings BAAI/bge-small-en-v1.5 + Index FAISS
                                            └── Rapprochement sémantique des cas historiques
                                                        │
                                                        ▼
                                         [ Agent 5: Medical Reasoning LLM ]
                                            ├── Synthèse clinique par Qwen2.5-3B-Instruct
                                            ├── Prompt engineering à schéma contraint JSON
                                            └── Justification différentielle et recommandations
                                                        │
                                                        ▼
                                         [ Agent 6: Quality & Safety Agent ]
                                            ├── Audit déterministe (10 garde-fous cliniques)
                                            ├── Détection d'hallucinations & isolation des données
                                            └── Boucle de révision active (2 passes max)
                                                        │
                                                        ▼
                                         [ Agent 7: Box 7 Medical Report ]
                                            ├── Compte-rendu clinique HTML interactif
                                            ├── Enregistrement structuré JSON (Dossier Patient)
                                            └── Clause d'audit : human_review_required: true
                                                        │
                                                        ▼
                                         [ Orchestrateur Hospitalier n8n ]
                                            ├── URGENT     ➔ Alerte Biopsie & Convocation RCP
                                            ├── SURV       ➔ Programmation Échographie à 6 Mois
                                            └── ROUTINE    ➔ Dépistage Annuel Standardisé
                                                        │
                                                        ▼
                                         [ Notification Automatique Sécurisée ]
                                            └── Envoi au Radiologue Référent / Archive PACS-RIS
```

---

## 🚀 Fonctionnalités Majeures

1. **Réseau de Vision Multimodal (ResNet-18 Dual-Branch) :**
   * Traitement conjoint des paires mammographie / échographie pour une classification granulaire BI-RADS (1, 2, 3, 4A, 4B, 4C, 5, 6).
   * **Gain multimodal :** $\text{ROC-AUC} = 0.820$ (contre $0.792$ en mammographie seule et $0.674$ en échographie seule).
2. **Explicabilité Radiologique (Grad-CAM XAI) :**
   * Génération temps réel des zones d'activation thermique superposées aux clichés.
   * **87.4% de concentration d'énergie** confinée au parenchyme tumoral vérifié.
3. **Moteur RAG Clinique Déterministe :**
   * Indexation vectorielle dense FAISS alimentée par les recommandations officielles de l'American College of Radiology (ACR).
   * Justification systématique des conduites à tenir selon les descripteurs sémantiques.
4. **Agent de Sécurité & Boucle de Rétroaction :**
   * Validation de 10 points de contrôle critiques (intégrité des métadonnées, concordance des probabilités, masquage de données sensibles).
   * **100% de résistance** aux attaques adversariales simulées (10/10).
5. **Orchestration d'Urgence Hospitalière (n8n) :**
   * Workflow automatisé à 8 nœuds déployé sous n8n (`http://localhost:5678`).
   * Routage conditionnel instantané : alerte RCP pour BI-RADS 4/5 vs convocation de contrôle à 6 mois pour BI-RADS 3.
6. **Interface Web Clinique & Portail Bilingue :**
   * Console d'ingestion et d'analyse en direct sur `http://localhost:8000/form`.
   * Portail des rapports académiques bilingues (FR/EN) sur `http://localhost:8000/report/technical-report`.

---

## 📊 Résultats & Benchmark de l'Équipe

Sur la cohorte binationale de **332 patientes** (2 001 clichés, 321 comptes-rendus assainis, 12.11 Go) :

| Approche / Modalité | Exactitude (Acc) | Sensibilité (Se) | Spécificité (Sp) | ROC-AUC | F1-Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Échographie Seule (US) | 68.4% | 72.1% | 65.3% | 0.674 | 0.686 |
| Mammographie Seule (FFDM) | 79.8% | 84.6% | 75.9% | 0.792 | 0.801 |
| **Fusion Multimodale BCMID (Dual-ResNet-18)** | **84.2%** | **91.5%** | **78.3%** | **0.820** | **0.846** |

### Stratification Patient (Zéro Fuite / Zero-Leakage)
* **Train Set (70%) :** 228 patientes
* **Validation Set (15%) :** 47 patientes
* **Test Set Hold-Out (15%) :** 57 patientes *(strictement invisibles à l'entraînement)*
* **Garantie de non-chevauchement :** `leakage = 0` vérifié par test unitaire automatique.

---

## 📑 Rapports Techniques Officiels (12 Pages)

Les livrables académiques de référence du projet sont disponibles en téléchargement direct :

| Livrable | Langue | Description | Lien Direct |
| :--- | :---: | :--- | :--- |
| **BCMID Rapport Final Condensé** | 🇫🇷 Français | Rapport académique officiel complet (12 pages, figures, tableaux et méthodologie) | [Télécharger (PDF FR)](http://localhost:8000/report/technical-report-fr/pdf) |
| **BCMID Academic Project Report** | 🇬🇧 Anglais | Official English translated technical report (12 pages, matching typography and XAI figures) | [Download (PDF EN)](http://localhost:8000/report/technical-report/pdf?lang=en) |
| **Code Source LaTeX** | 📄 LaTeX | Archive source `.tex` avec tableaux quadrillés complets et diagrammes vectoriels TikZ | [Télécharger (.tex)](http://localhost:8000/report/latex) |
| **Portail Bilingue** | 🌐 Web | Interface interactive de sélection et téléchargement des rapports | [Accéder au Portail](http://localhost:8000/report/technical-report) |

---

## 🗂️ Structure du Répertoire

```
deeplearning5eme/
├── api_server.py                 # Serveur FastAPI (Microservices Blocs 1 à 7 + Triage)
├── n8n_bcmid_workflow.json       # Workflow d'orchestration officiel n8n (8 nœuds)
├── requirements.txt              # Dépendances Python de production
├── config.yaml                   # Configuration globale du pipeline
├── BCMID_annotations.tsv        # Métadonnées cliniques et vérités terrain BI-RADS
├── README.md                     # Documentation officielle du projet de groupe
├── BCMID_Technical_Report.tex    # Fichier source LaTeX du rapport technique
│
├── clinical_pipeline/            # Agents cliniques modulaires (ex-ikbelwork)
│   ├── clinical_rag_enhancer.py  # Agent 4 : Moteur RAG Vectoriel (ACR BI-RADS)
│   ├── safety_agent.py           # Agent 6 : Agent de Sécurité & Contrôle Qualité
│   ├── medical_report_generator.py # Agent 7 : Générateur de compte-rendu Box 7
│   ├── run_orchestrator.py       # Orchestrateur d'exécution de bout en bout
│   └── acr_birads_guidelines.json # Base de connaissances sémantique ACR
│
├── dq_agent/                     # Agent 1 : Data & Quality Processing Agent
│   ├── anonymize.py              # Pseudonymisation salée SHA-256
│   ├── integrity.py              # Détection d'images corrompues et doublons
│   ├── preprocess.py             # Rehaussement CLAHE et filtrage médian
│   └── splits.py                 # Partitionnement stratifié patient sans fuite
│
├── bcmid_work/                   # Espace de travail, rapports et index FAISS
│   ├── reports/
│   │   ├── form.html             # Console web d'ingestion clinique temps réel
│   │   ├── BCMID_Rapport_Final_Condense.pdf # Rapport officiel français (12p)
│   │   ├── BCMID_Rapport_Final_EN.pdf       # Rapport officiel anglais (12p)
│   │   └── medical_report_*.html # Comptes-rendus médicaux HTML générés
│   ├── manifest.csv              # Manifeste vérifié du jeu de données (332 patientes)
│   ├── splits.json               # Découpage officiel zéro fuite (70/15/15)
│   └── final_medical_reports.json# 20 comptes-rendus de référence
│
├── sample_data/                  # Cas cliniques d'évaluation (Hold-out Test Set)
│   ├── 1_CAS_MALADE_URGENT_P1eb742860c/  # Cas BI-RADS 5 Malade / Urgent
│   ├── 2_CAS_SURVEILLANCE_Pf9bea655cf/   # Cas BI-RADS 3 Surveillance
│   └── 3_CAS_ROUTINE_SAIN_Paacb1ec57b/   # Cas BI-RADS 1 Routine / Sain
│
├── scripts/                      # Scripts d'automatisation et de compilation PDF
│   ├── generate_translated_english_report_pdf.py # Générateur du rapport 12p EN
│   ├── generate_dq_report_pdf.py                 # Générateur du rapport Data Quality
│   └── generate_rag_report_pdf.py                # Générateur du rapport RAG & Agents
│
└── tests/                        # Suite complète de tests unitaires (61 tests)
    ├── test_anonymize.py         # Tests de pseudonymisation SHA-256
    ├── test_ingestion_agent.py   # Tests de validation de l'ingestion
    ├── test_integrity.py         # Tests de détection de corruption d'image
    ├── test_modality.py          # Tests de vérification de modalité
    ├── test_preprocess.py        # Tests des algorithmes CLAHE et médian
    ├── test_report.py            # Tests de conformité des comptes-rendus Box 7
    ├── test_safety_pipeline.py   # Tests des 10 garde-fous de l'agent de sécurité
    ├── test_splits.py            # Tests d'absence absolue de fuite de données
    ├── test_validation.py        # Tests de validation des schémas JSON
    └── test_vision_agent.py      # Tests du modèle de vision et de Grad-CAM
```

---

## ⚡ Guide de Démarrage Rapide

### 1. Cloner le Dépôt & Installer l'Environnement
```bash
git clone https://github.com/mohamedmalekh/bcmid-multimodal-medical-ai.git
cd bcmid-multimodal-medical-ai

# Créer un environnement virtuel Python 3.10+
python -m venv venv

# Activer l'environnement
# Sur Linux / macOS :
source venv/bin/activate
# Sur Windows (PowerShell) :
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Lancer la Suite de Tests Unitaires
```bash
python -m pytest tests -v
```
> **Résultat attendu :** `61 passed in ~1.5s` (100% de succès sur tous les modules).

### 3. Démarrer le Serveur Microservices FastAPI
```bash
python api_server.py
```
* **Documentation interactive Swagger :** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Console d'ingestion clinique :** [http://localhost:8000/form](http://localhost:8000/form)
* **Portail des rapports académiques :** [http://localhost:8000/report/technical-report](http://localhost:8000/report/technical-report)

### 4. Démarrer & Importer le Workflow n8n
1. Lancer l'instance n8n locale :
   ```bash
   npx n8n
   ```
2. Ouvrir votre navigateur sur [http://localhost:5678](http://localhost:5678).
3. Dans le menu contextuel en haut à droite (`...`), choisir **Import from File** et sélectionner `n8n_bcmid_workflow.json`.
4. Cliquer sur **Publish** pour activer le webhook de routage hospitalier.

---

## 🧪 Cas Cliniques de Référence (Benchmark)

| Cas Test | ID Patiente | Diagnostic Réel | BI-RADS Prédit | Priorité n8n | Conduite Clinique Recommandée |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Cas Malade (Urgent)** | `P1eb742860c` | Carcinome Infiltrant | **BI-RADS 5** (94.2%) | **`URGENT`** | Macro-biopsie percutanée guidée sous échographie sous 72h + Réunion de Concertation Pluridisciplinaire (RCP). |
| **Cas Surveillance** | `Pf9bea655cf` | Fibroadénome Évolutif | **BI-RADS 3** (78.1%) | **`SURVEILLANCE`** | Contrôle échographique unilatéral à 6 mois pour évaluer la stabilité morphologique. |
| **Cas Sain (Routine)** | `Paacb1ec57b` | Tissu Graisseux Normal | **BI-RADS 1** (94.0%) | **`ROUTINE`** | Poursuite du dépistage mammographique biennal standardisé selon le calendrier national. |

---

## 🛡️ Avertissement Réglementaire & Déontologique

Ce logiciel a été développé dans un cadre académique et scientifique strict au sein d'**ESPRIT**. En accord avec les exigences des dispositifs médicaux logiciels (**SaMD Classe IIa, directive européenne MDR 2017/745**) :
* Le système est un **outil d'aide à la décision clinique (CDSS)** et non un automate diagnostique autonome.
* L'ensemble des prédictions, cartes Grad-CAM, analyses différentielles et orientations de triage **doivent obligatoirement être validées et signées par un radiologue ou sénologue diplômé** (`human_review_required: true`).
* Aucune donnée nominative de patiente n'est conservée en clair : les identifiants font l'objet d'un hachage cryptographique irréversible salé SHA-256.

---

## 🏛️ Institution & Mentions Légales

* **Établissement :** [ESPRIT (École Supérieure Privée d'Ingénierie et de Technologies)](https://esprit.tn)
* **Département :** Département Informatique & Télécommunications
* **Spécialité :** 5\textsuperscript{ème} Année — Data Science, Deep Learning & Intelligence Artificielle
* **Année Académique :** 2026 – 2027
* **Licence :** Usage Académique et de Recherche Médicale
