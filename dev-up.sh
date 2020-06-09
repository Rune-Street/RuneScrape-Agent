cd "${0%/*}"

export RUNESCRAPE_SERVICE=localhost
export RUNESCRAPE_ENDPOINT=items/history
export RUNESCRAPE_PORT=8000
python3 runescrape-agent/agent.py
