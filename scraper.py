import logging

import arrow
import requests

logger = logging.getLogger(__name__)

API_URL = "https://opendata.reseaux-energies.fr/api/records/1.0/search/"

LIVE_DATASET = "eco2mix-regional-tr"
CONSOLIDATED_DATASET = "eco2mix-regional-cons-def"


def query_regional_production_live(reference_datetime: arrow.Arrow):
    """Query regional data on production on the past day.
    This will create duplicates."""
    logger.debug(f"querying live data for {reference_datetime} ")
    params = {
        "dataset": LIVE_DATASET,
        "q": get_datetime_query_param(reference_datetime, interval_days=1),
    }
    res = requests.get(API_URL, params=params)
    return res.json()


def get_datetime_query_param(end_datetime: arrow.Arrow, interval_days: int = 1) -> str:
    start = end_datetime.shift(days=-interval_days).format("YYYY-MM-DDTHH:mm")
    end = end_datetime.format("YYYY-MM-DDTHH:mm")
    return f"date_heure:[{start} TO {end}]"
