from fastapi import APIRouter, HTTPException
from app.models.prospeo_models import EnrichRequest, EnrichListRequest, ProspeoResult
from app.services.prospeo_service import prospeo_service
from app.config import settings

router = APIRouter(prefix="/enrich", tags=["enrich"])


@router.post("", response_model=ProspeoResult)
def enrich_single(request: EnrichRequest):
    """Enrich a single LinkedIn URL"""
    if not settings.PROSPEO_API_KEY:
        raise HTTPException(status_code=500, detail="PROSPEO_API_KEY not configured")

    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Enrich request for: {request.linkedin_url}")
    try:
        return prospeo_service.enrich_person(request.linkedin_url)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/batch", response_model=list[ProspeoResult])
def enrich_batch(request: EnrichListRequest):
    """Enrich multiple LinkedIn URLs"""
    if not settings.PROSPEO_API_KEY:
        raise HTTPException(status_code=500, detail="PROSPEO_API_KEY not configured")

    if not request.urls:
        raise HTTPException(status_code=400, detail="No URLs provided")

    return prospeo_service.enrich_list(request.urls)
