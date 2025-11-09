# AI Experimentation Copilot MVP (Ollama)

Minimal MVP that ingests a 2-variant A/B test CSV, computes stats, and produces:
- Structured summary (JSON)
- Three next-test suggestions (JSON)

## Prerequisites
- Python 3.10+
- Ollama installed and running
- Pull a local model: `ollama pull llama3`

## Setup
```bash
cd copilot_mvp
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python app.py --csv data/sample_ab_win.csv --model llama3
python app.py --csv data/sample_ab_borderline.csv --model llama3
python app.py --csv data/sample_ab_loss.csv --model llama3
```
Outputs are printed to console and saved under `outputs/`.
