"""
Configuration management for the outreach tool.
Loads/saves config.json with defaults for profile, credentials, and settings.
"""

import json
import os

DATA_DIR = os.environ.get("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(DATA_DIR, "config.json")

DEFAULT_CONFIG = {
    "gmail_address": "",
    "gmail_app_password": "",
    "groq_api_key": "",
    "groq_api_key_2": "",
    "groq_api_key_3": "",
    "gemini_api_key": "",
    "cerebras_api_key": "",
    "send_delay_seconds": 60,
    "profile": {
        "name": "",
        "college": "",
        "branch": "",
        "year": "",
        "cgpa": "",
        "skills": "",
        "github": "",
        "linkedin": "",
        "bio": ""
    },
    "resume_path": os.path.join(DATA_DIR, "uploads", "resume.pdf"),
    "resume_parsed": {}
}


def _env_defaults():
    """Populate default values from environment variables if present."""
    env_map = {
        "gmail_address": os.environ.get("GMAIL_ADDRESS", ""),
        "gmail_app_password": os.environ.get("GMAIL_APP_PASSWORD", ""),
        "groq_api_key": os.environ.get("GROQ_API_KEY", ""),
        "groq_api_key_2": os.environ.get("GROQ_API_KEY_2", ""),
        "groq_api_key_3": os.environ.get("GROQ_API_KEY_3", ""),
        "gemini_api_key": os.environ.get("GEMINI_API_KEY", ""),
        "cerebras_api_key": os.environ.get("CEREBRAS_API_KEY", ""),
    }
    if os.environ.get("SEND_DELAY_SECONDS"):
        try:
            env_map["send_delay_seconds"] = int(os.environ.get("SEND_DELAY_SECONDS"))
        except ValueError:
            pass
    return {k: v for k, v in env_map.items() if v}


def load_config():
    """Load config from disk. Create with defaults/env vars if missing."""
    env_overrides = _env_defaults()

    if not os.path.exists(CONFIG_PATH):
        cfg = DEFAULT_CONFIG.copy()
        cfg.update(env_overrides)
        save_config(cfg)
        return cfg

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Merge with defaults to handle missing keys after upgrades
    merged = DEFAULT_CONFIG.copy()
    merged.update(config)

    # Fill in any missing/empty keys with environment variables if available
    for k, v in env_overrides.items():
        if not merged.get(k):
            merged[k] = v

    if "profile" in config:
        merged_profile = DEFAULT_CONFIG["profile"].copy()
        merged_profile.update(config["profile"])
        merged["profile"] = merged_profile

    return merged


def save_config(config):
    """Persist config to disk."""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def is_profile_complete(config):
    """Check if the minimum profile fields are filled."""
    profile = config.get("profile", {})
    required = ["name", "college", "branch", "year", "skills", "bio"]
    return all(profile.get(field, "").strip() for field in required)


def is_settings_complete(config):
    """Check if Gmail + Gemini credentials are configured."""
    return bool(
        config.get("gmail_address", "").strip()
        and config.get("gmail_app_password", "").strip()
        and config.get("groq_api_key", "").strip()
    )
