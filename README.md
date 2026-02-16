LUNA — Web deployment

Quick start (local):

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the web app:

```powershell
python web_app\app.py
```

3. Open http://localhost:5000 in your browser.

Expose to the internet (optional):
- Install ngrok and run `ngrok http 5000` to get a public URL.

Learning features:
- Use `learn: <fact>` to save a fact to memory.
- Use `search: <term>` to find learned facts.
