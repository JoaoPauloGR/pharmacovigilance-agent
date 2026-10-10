# FAERS AI Agent
 
A learning project focused on building, testing and operating an AI agent on top of public pharmacovigilance data from the FDA Adverse Event Reporting System (FAERS), using locally hosted language models.
 
> **Disclaimer:** This is an educational project. It is not a medical device and must not be used for clinical, regulatory or treatment decisions. FAERS reports are voluntary and unverified, and a report does not establish that a drug caused an adverse event.
 
---
 
## Why this project
 
The goal is less about the final answers and more about the engineering behind them:
 
- **Implementing agents** — tool design, routing, orchestration and failure handling.
- **Sustaining agents** — testing, evaluation, observability and change management over time.
- **Running AI locally** — serving open-weight models on local hardware and understanding the trade-offs against hosted APIs.
- **Assessing risk** — studying the risks of using AI in regulated laboratory environments, such as those supported by LIMS platforms.
## Architecture
 
The agent receives a natural-language question, decides which tool (or combination of tools) to use, and composes an answer grounded in the tool outputs.
 
```
                    ┌──────────────────────┐
     User  ───────► │       AI Agent       │
                    │   (local LLM + tool  │
                    │      orchestration)  │
                    └──────────┬───────────┘
          ┌──────────────┬─────┴─────────┬──────────────────┐
          ▼              ▼               ▼                  ▼
   ┌────────────┐ ┌─────────────┐ ┌──────────────┐ ┌─────────────────┐
   │  openFDA   │ │ ML Predict  │ │ Text-to-SQL  │ │  Drug Label RAG │
   │  API tool  │ │    tool     │ │     tool     │ │      tool       │
   └────────────┘ └─────────────┘ └──────────────┘ └─────────────────┘
```
 
### Tools
 
| Tool | Description |
|------|-------------|
| **openFDA API** | Queries the openFDA endpoints for up-to-date adverse event reports. |
| **ML prediction** | Runs a machine learning model trained on FAERS data to produce predictions (e.g. likelihood of a serious outcome given drug and patient features). |
| **Text-to-SQL** | Translates natural-language questions into SQL and runs them against a local database built from FAERS quarterly files. |
| **Drug label RAG** | Retrieval-augmented generation over drug package inserts (labels), with answers citing the retrieved passages. The RAG pipeline (ingestion, chunking, embeddings, retrieval) is built as part of this project. |
 
## Quality and robustness
 
The agent is treated as production software, not a notebook experiment:
 
- **Unit tests** for each tool, parser and data transformation.
- **Integration tests** covering end-to-end agent flows, including tool selection and error paths.
- **Evals** to compare local models on accuracy, tool-selection quality, groundedness and latency, using a fixed, versioned question set.
- **Guardrails** for SQL safety (read-only access, query validation) and for out-of-scope or unsafe requests.