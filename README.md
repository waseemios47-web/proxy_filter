# Proxy Filter Streamlit App

Upload a TXT file containing mixed proxy formats:
- http://
- socks4://
- socks5://

The app automatically:
- Cleans protocol prefixes
- Separates proxies by type
- Downloads 3 TXT files

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
