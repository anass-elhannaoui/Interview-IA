# AI Interview Assistant

I built a lightweight Streamlit app to simulate HR-style interviews and give AI-powered feedback.

## What it does
- I collect candidate info (name, experience, skills, target role/company).
- The app runs a short structured interview (you answer 5 questions).
- At the end it generates a scored feedback summary.

## Files
- `app.py` — main Streamlit application (UI + OpenAI integration).
- `.gitignore` — I ignore the `.streamlit/` folder so secrets/config aren't committed.
- (optional) `requirements.txt` — save your env if you want reproducible installs.

## Prereqs
- Python 3.10+ recommended
- Streamlit
- OpenAI Python SDK (match version used in `app.py`)
- Windows (instructions below use PowerShell)

## Install (quick)
```powershell
cd "C:\Users\yoga\Desktop\IA Engineer\LLM Engineering"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install streamlit openai streamlit-js-eval
```

(Optional) Save deps:
```powershell
pip freeze > requirements.txt
```

## Configure the OpenAI key
I keep the API key out of source control using Streamlit secrets.

Create `.streamlit/secrets.toml` (this folder is ignored by `.gitignore`):

```toml
# filepath: c:\Users\yoga\Desktop\IA Engineer\LLM Engineering\.streamlit\secrets.toml
OPENAI_API_KEY = "sk-REPLACE_WITH_YOUR_KEY"
```

Or set an environment variable in PowerShell:
```powershell
$env:OPENAI_API_KEY="sk-REPLACE_WITH_YOUR_KEY"
```

## Run the app
From the project root (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

## Notes & troubleshooting
- You may see "missing ScriptRunContext" warnings in some environments — they are usually harmless. Make sure you start the app with `streamlit run app.py`.
- If you get API errors, confirm `OPENAI_API_KEY` is set and valid.
- If you accidentally committed secrets, remove them and rotate the key. Example to stop tracking:
```powershell
git rm --cached .streamlit/secrets.toml
git commit -m "Remove secrets from repo"
```

## Security
- Never commit `.streamlit/secrets.toml` or any file with secret keys.
- My `.gitignore` includes `.streamlit/` so secrets won't be tracked by default.

