# Song downloader
## About
Input youtube or soundcloud url to download song 

## Run
1. (Optional) Create a virtual environment
```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Install [yt-dlp](https://github.com/yt-dlp/yt-dlp)
Macos: `brew install yt-dlp`

4. Run
```bash
./scripts/run.sh
```