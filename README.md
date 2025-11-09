# AI Experimentation Copilot (Local MVP)

An open-source **AI Copilot for Experimentation & A/B Testing**, built with **LangChain + Ollama + Python**.  
It summarizes A/B test results, retrieves insights from past experiments (RAG), and suggests the next best experiments — all locally in Jupyter Notebook.

---

## Features

**Automated A/B Test Summaries**  
**Smart Test Recommendations (RAG)**  
**Fully Local Stack**  
**Extendable Design**  

---

## Project Structure

```
ai-experiment-copilot/
│
├── copilot_notebook.ipynb
├── data/
├── rag/
├── outputs/
├── src/
├── requirements.txt
└── README.md
```

---

## Setup

1️⃣ Install [Ollama](https://ollama.ai) and pull a model:  
```bash
ollama pull llama3
```

2️⃣ Install dependencies:  
```bash
pip install -r requirements.txt
```

---

## Usage

1. Launch Jupyter and open the notebook:  
   ```bash
   jupyter notebook copilot_notebook.ipynb
   ```

2. Drop your CSV test data in `/data/`:
   ```csv
   variant,n,conversions,experiment_name,hypothesis,primary_metric
   control,12450,842,"Pricing: $49 vs $39","Lowering price increases purchase rate","conversion_rate"
   treatment,12380,955,"Pricing: $49 vs $39","Lowering price increases purchase rate","conversion_rate"
   ```

3. Add past learnings in `/rag/past_experiments.jsonl`

4. Run:
   ```python
   bundle = run_one("data/your_pricing_test.csv", model_name="llama3")
   ```

5. View outputs in `/outputs/`

---

## How It Works

1. Compute stats (z-test)  
2. Generate summary via LLM  
3. Retrieve past learnings via TF-IDF RAG  
4. Suggest next tests

---

## Dependencies

```
pandas==2.2.2
scipy==1.11.4
scikit-learn==1.5.2
langchain==0.2.10
langchain-core==0.2.10
langchain-ollama==0.1.0
pydantic==2.7.0
```

---

## 📄 License

MIT License © 2025 Abhinav Sharma
