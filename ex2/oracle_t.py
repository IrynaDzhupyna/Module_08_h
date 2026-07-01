import os
import sys
from dotenv import load_dotenv


def get_config(required_keys: list[str]) -> dict[str, str]:
    config = {}

    for key in required_keys:
        config[key] = os.getenv(key)

    return config


def validate_config(config: dict[str, str]) -> list[str]:
    missing = []

    for key, value in config.items():
        if not value:
            missing.append(key)

    return missing

def main() -> None:
    pre_dotenv_env = set(os.environ.keys())
    load_dotenv()
    
    print("ORACLE STATUS: Reading the Matrix...")
    required_keys = [
            "MATRIX_MODE",
            "DATABASE_URL",
            "API_KEY",
            "LOG_LEVEL",
            "ZION_ENDPOINT"]
    config = get_config(required_keys)

    missing = validate_config(config)
    if missing:
        print("\nWARNING: Missing configurations!\n")
        for element in missing:
            print(f" - {element}")

        print("\nCreate a .env file or define the missing enviroment variables.")
        sys.exit(1)
    print_configurations(config)

if __name__ == "__main__":
    main()
