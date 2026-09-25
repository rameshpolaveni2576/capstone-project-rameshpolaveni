# Zepto Data & AI Platform

This repository contains one connected capstone with three linked modules that read as one story:

- `data_pipeline`: scrape raw catalog data, clean and normalize it, convert the required fixed-rate price field, and load it into a relational SQLite store.
- `analytics`: load the Titanic dataset once, profile and clean it, run the EDA story, and train/evaluate predictive models plus a regression side-task.
- `support_assistant`: build a grounded policy assistant over Zepto's local policy corpus using ChromaDB + embeddings + a LangGraph flow with a mock LLM baseline.

The project uses one consolidated dependency file at the repository root: `requirements.txt`.

## Setup

```bash
python -m venv .venv
# Windows PowerShell:
# .\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
```

## Run each module

### 1) Data pipeline

```bash
python data_pipeline/build_database.py
```

This script scrapes the public Books to Scrape catalog, cleans the extracted fields, applies the required fixed-rate conversion `1 GBP = 105.50 INR`, stores the normalized SQLite database, and saves the SQL query outputs in `data_pipeline/queries_output.md`.

### 2) Analytics pipeline

```bash
python analytics/02_modeling.py
```

This script reads the committed offline fallback file `analytics/titanic.csv`, runs the Titanic EDA/modeling workflow, saves the model comparison CSV, generates the chart artifacts, and writes the final joblib pipeline artifact to `analytics/best_titanic_pipeline.joblib`.

### 3) Support assistant

```bash
$env:MOCK_LLM = "1"
uvicorn support_assistant.main:app --host 127.0.0.1 --port 7860
```

Then call the local endpoint:

```bash
curl -X POST http://127.0.0.1:7860/ask -H "Content-Type: application/json" -d '{"query": "What is the delivery fee for orders below INR 149?"}'
```

## Design decisions

### Data pipeline design

The pipeline uses `requests` and `BeautifulSoup` to scrape multiple category pages, handles messy fields with median imputation or row filtering, converts `price_gbp` to `price_inr` using the required project-defined fixed rate, and stores the data in a normalized two-table SQLite schema with a category-to-book relationship.

### Analytics design

The analytics workflow loads the Titanic dataset once, saves it as `analytics/titanic.csv`, performs missing-value handling and visual profiling, then continues into a full modeling pass with train/test stratification, preprocessing inside pipelines, classifier comparison, imbalance testing, a RandomForest tuning step using `GridSearchCV`, a regression side-task predicting `fare`, and a final saved end-to-end joblib pipeline.

### Support assistant design

The support assistant ingests Zepto policy documents, chunks them, embeds the chunks with `sentence-transformers/all-MiniLM-L6-v2`, stores them in ChromaDB, and routes queries through a LangGraph graph where `classify_intent` sends policy questions to `retrieve_and_answer` and all other questions to `direct_answer`. The default baseline uses `MOCK_LLM=1`, which avoids external API calls and uses deterministic mock logic and validated JSON output.

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── Project Description.txt
├── data_pipeline/
│   ├── build_database.py
│   ├── README.md
│   ├── queries_output.md
│   └── zepto_books.db
├── analytics/
│   ├── 01_eda.py
│   ├── 02_modeling.py
│   ├── README.md
│   ├── titanic.csv
│   ├── classifier_comparison.csv
│   ├── best_titanic_pipeline.joblib
│   └── *.png
├── support_assistant/
│   ├── Dockerfile
│   ├── main.py
│   ├── README.md
│   ├── docs/
│   └── chroma_store/
└── .gitignore
```

## Notes

This is a single-repository submission with all three modules living at the root under their own folders, as required by the capstone brief. The implementation uses one consolidated `requirements.txt` for shared dependencies and keeps all required narrative explanations in Markdown files within the repo rather than in separate document files.
