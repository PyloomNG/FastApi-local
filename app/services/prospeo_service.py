import time
import requests
from app.config import settings
from app.models.prospeo_models import ProspeoResult


class ProspeoService:
    def __init__(self):
        self.api_key = settings.PROSPEO_API_KEY
        self.endpoint = settings.PROSPEO_ENDPOINT
        self.max_retries = settings.PROSPEO_MAX_RETRIES
        self.delay = settings.PROSPEO_DELAY_BETWEEN_REQUESTS

    def enrich_person(self, linkedin_url: str) -> ProspeoResult:
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Using endpoint: {self.endpoint}")
        logger.info(f"API key: {self.api_key[:10]}...")
        headers = {
            "X-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        body = {
            "only_verified_email": False,
            "data": {"linkedin_url": linkedin_url}
        }

        logger.info(f"Request body: {body}")
        for attempt in range(1, self.max_retries + 1):
            logger.info(f"Attempt {attempt}: calling {self.endpoint}")
            response = requests.post(self.endpoint, headers=headers, json=body)
            logger.info(f"Response status: {response.status_code}")

            if response.status_code == 429:
                wait = 10 * attempt
                print(f"   Rate limit (attempt {attempt}/{self.max_retries}). Waiting {wait}s...")
                time.sleep(wait)
                continue

            if response.status_code != 200:
                raise Exception(f"Prospeo error: {response.status_code} - {response.text}")

            break
        else:
            raise Exception("Rate limit exceeded after 3 retries.")

        data = response.json()
        person = data.get("person") or {}
        email = person.get("email") or {}
        mobile = person.get("mobile") or {}

        return ProspeoResult(
            linkedin_url=linkedin_url,
            person_id=person.get("person_id"),
            first_name=person.get("first_name"),
            last_name=person.get("last_name"),
            full_name=person.get("full_name"),
            email_status=email.get("status"),
            email=email.get("email"),
            mobile_status=mobile.get("status"),
            mobile=mobile.get("mobile"),
        )

    def enrich_list(self, urls: list[str]) -> list[ProspeoResult]:
        results = []

        for i, url in enumerate(urls):
            print(f"Processing {i + 1}/{len(urls)}: {url}")
            try:
                result = self.enrich_person(url)
                results.append(result)
            except Exception as e:
                print(f"Error enriching {url}: {e}")
                results.append(ProspeoResult(linkedin_url=url))

            if i < len(urls) - 1:
                time.sleep(self.delay)

        return results


prospeo_service = ProspeoService()
