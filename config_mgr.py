import json
import os

CONFIG_FILE = 'config.json'

DEFAULT_CONFIG = {
    'shortcut': 'alt+shift+h',
    'behavior': 'fade',  # 'fade' (disappears after a few secs) or 'persist' (stays until closed)
    'fade_timeout': 3.0  # seconds
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            for k, v in DEFAULT_CONFIG.items():
                if k not in config:
                    config[k] = v
            return config
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
