import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Prospeo API
    PROSPEO_API_KEY: str = os.getenv("PROSPEO_API_KEY", "")
    PROSPEO_ENDPOINT: str = os.getenv("PROSPEO_ENDPOINT", "https://api.prospeo.io/v1/person/enrich")
    PROSPEO_MAX_RETRIES: int = int(os.getenv("PROSPEO_MAX_RETRIES", "3"))
    PROSPEO_DELAY_BETWEEN_REQUESTS: int = int(os.getenv("PROSPEO_DELAY_BETWEEN_REQUESTS", "2"))

    # App
    APP_NAME: str = "Prospeo Enrich API"
    APP_VERSION: str = "1.0.0"

    # Bulk paths
    BASE_DIR: Path = Path(__file__).parent.parent
    INPUT_EXCEL: Path = BASE_DIR / "data" / "input.xlsx"
    OUTPUT_EXCEL: Path = BASE_DIR / "data" / "enriched_output.xlsx"


settings = Settings()
