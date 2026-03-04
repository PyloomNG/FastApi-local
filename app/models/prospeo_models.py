from pydantic import BaseModel
from typing import Optional


class ProspeoResult(BaseModel):
    linkedin_url: str
    person_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    email_status: Optional[str] = None
    email: Optional[str] = None
    mobile_status: Optional[str] = None
    mobile: Optional[str] = None


class EnrichRequest(BaseModel):
    linkedin_url: str


class EnrichListRequest(BaseModel):
    urls: list[str]
