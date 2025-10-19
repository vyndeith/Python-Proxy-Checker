# Simple HTTP Proxy Checker

What it does

- Reads URLs from `links.txt` (one URL per line, ONLY RAW .txt FILES!!).
- Downloads proxy lists from each URL, checks each proxy.
- Appends working proxies to `proxies.txt` next to `main.py`.

Quick start

```powershell
pip install requests
python main.py
```

`links.txt` format
- One URL per line. Each URL should return a plain-text list of proxies (one proxy per line).

Output
- `proxies.txt` is created next to `main.py` (if missing) and new working proxies are appended.

Notes
- Adjust `TIMEOUT` and `FETCH_TIMEOUT` in `main.py` if needed.
- The script avoids duplicate writes during a single run, but does not persist duplicates across runs unless you keep `proxies.txt`.