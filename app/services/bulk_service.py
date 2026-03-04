import time
from typing import Union
import pandas as pd
import numpy as np
import requests
from app.config import settings


class BulkService:
    def __init__(self):
        self.api_key = settings.PROSPEO_API_KEY
        self.endpoint = settings.PROSPEO_ENDPOINT
        self.max_retries = settings.PROSPEO_MAX_RETRIES

    def _clean_linkedin_url(self, url: str) -> str:
        """Extract base LinkedIn URL without extra parameters"""
        # Remove query parameters like ?miniProfileUrn=...
        if "?" in url:
            url = url.split("?")[0]
        # Ensure URL ends with /
        if not url.endswith("/"):
            url += "/"
        return url

    def _enrich_single(self, linkedin_url: str) -> dict:
        """Enrich a single LinkedIn URL"""
        # Clean URL to remove extra parameters
        clean_url = self._clean_linkedin_url(linkedin_url)
        print(f"   Clean URL: {clean_url}")
        headers = {
            "X-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        body = {
            "only_verified_email": False,
            "data": {"linkedin_url": clean_url}
        }

        for attempt in range(1, self.max_retries + 1):
            response = requests.post(self.endpoint, headers=headers, json=body)

            if response.status_code == 429:
                wait = 10 * attempt
                print(f"   Rate limit (attempt {attempt}/{self.max_retries}). Waiting {wait}s...")
                time.sleep(wait)
                continue

            if response.status_code != 200:
                print(f"   Error: {response.status_code} - {response.text}")
                return {"email": None, "verified_email": None, "phone": None}

            break
        else:
            return {"email": None, "verified_email": None, "phone": None}

        try:
            data = response.json()
            person = data.get("person") or {}
            email = person.get("email") or {}
            mobile = person.get("mobile") or {}

            # Extraer email y status
            email_value = email.get("email")
            email_status = email.get("status")

            # Extraer phone y status
            phone_value = mobile.get("mobile")
            phone_status = mobile.get("status")

            return {
                "email": email_value,
                "email_status": email_status,
                "phone": phone_value,
                "phone_status": phone_status
            }
        except Exception as e:
            print(f"   Parse error: {e}")
            return {"email": None, "email_status": None, "phone": None, "phone_status": None}

    def enrich_excel(self, return_json: bool = False) -> Union[str, list[dict]]:
        """Process local Excel and save enriched version or return JSON"""
        input_path = settings.INPUT_EXCEL

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        df = pd.read_excel(input_path)

        # Ensure columns exist
        if "Email" not in df.columns:
            df["Email"] = None
        if "Verified Email" not in df.columns:
            df["Verified Email"] = None
        if "Phone" not in df.columns:
            df["Phone"] = None

        total = len(df)
        print(f"\nStarting enrichment of {total} records...")

        for i, row in df.iterrows():
            profile_url = row.get("profileUrl")

            if pd.isna(profile_url) or not profile_url:
                print(f"  [{i+1}/{total}] No URL, skipping...")
                continue

            print(f"  [{i+1}/{total}] Enriching: {profile_url}")

            result = self._enrich_single(profile_url)

            df.at[i, "Email"] = result["email"]
            df.at[i, "Email Status"] = result.get("email_status")
            df.at[i, "Phone"] = result["phone"]
            df.at[i, "Phone Status"] = result.get("phone_status")

            # Wait 10 seconds between each request
            if i < total - 1:
                print(f"    Waiting 10s...")
                time.sleep(10)

        # Return JSON if requested
        if return_json:
            # Replace NaN values with None for JSON serialization
            df_clean = df.replace({np.nan: None})
            return df_clean.to_dict(orient="records")

        # Save to file
        output_path = settings.OUTPUT_EXCEL
        df.to_excel(output_path, index=False)

        print(f"Enrichment completed! Output: {output_path}")
        return str(output_path)


bulk_service = BulkService()
