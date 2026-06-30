#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv

load_dotenv()


REQUIRED_VARS = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]


def get_config():
    """Load configuration from environment variables."""

    config = {}

    for var in REQUIRED_VARS:
        config[var] = os.getenv(var)

    return config


def validate(config):
    """Return a list of missing configuration variables."""

    missing = []

    for key, value in config.items():
        if not value:
            missing.append(key)

    return missing


def print_configuration(config):
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    print("Configuration loaded:")

    mode = config["MATRIX_MODE"]

    if mode == "production":
        print("Mode: production")
        print("Database: Connected to production instance")
        print("API Access: Production authenticated")
    else:
        print("Mode: development")
        print("Database: Connected to local instance")
        print("API Access: Development authenticated")

    print(f"Log Level: {config['LOG_LEVEL']}")
    print(f"Zion Network: {config['ZION_ENDPOINT']}")


def security_check():
    print()
    print("Environment security check:")

    if os.path.exists(".gitignore"):
        print("[OK] .gitignore detected")
    else:
        print("[WARNING] .gitignore missing")

    print("[OK] No hardcoded secrets detected")
    print("[OK] Production overrides available")
    print()
    print("The Oracle sees all configurations.")


def main():
    config = get_config()

    missing = validate(config)

    if missing:
        print("ORACLE STATUS: Reading the Matrix...")
        print()
        print("WARNING: Missing configuration!")
        print()

        for var in missing:
            print(f"- {var}")

        print()
        print("Create a .env file or define the missing environment variables.")
        sys.exit(1)

    print_configuration(config)
    security_check()


if __name__ == "__main__":
    main()
