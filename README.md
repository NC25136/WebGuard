# WebGuard 🛡️

WebGuard is an educational OSINT website safety checker built with Streamlit. It displays basic DNS, HTTPS, and HTTP status information and can look up an existing URL report through the VirusTotal API.

> **Disclaimer:** WebGuard is for educational use. A missing warning or report does not guarantee that a website is safe. Only analyze websites you are authorized to investigate.

## Run locally

1. Install Python 3.9 or later.
2. Clone this repository and open its directory.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and add your VirusTotal API key. The `.env` file is ignored by Git and should not be committed.

   ```bash
   cp .env.example .env
   ```

   Edit `.env` to set `VT_API_KEY` to your key. The VirusTotal lookup is optional; without a key, the app still displays the basic website information.

5. Start the app:

   ```bash
   streamlit run app.py
   ```

Streamlit will print a local URL (usually http://localhost:8501) to open in your browser.

## Deploy on Streamlit Community Cloud

1. Sign in to Streamlit Community Cloud and select this GitHub repository.
2. Set the app's main file to `app.py`.
3. In the app settings, add a secret named `VT_API_KEY` with your VirusTotal API key. Do not commit API keys to the repository.
4. Deploy. Streamlit Community Cloud installs the packages listed in `requirements.txt`.

## Project files

- `app.py` — Streamlit interface.
- `scanner.py` — URL validation and basic website checks.
- `reputation.py` — VirusTotal URL report lookup.
- `requirements.txt` — Python dependencies.
- `.env.example` — example environment configuration (not a real API key).
