from datetime import timedelta
import json

import arrow

from google.cloud import pubsub_v1
from google.oauth2.service_account import Credentials

import prefect
from prefect.core.parameter import DateTimeParameter
from prefect.run_configs import DockerRun
from prefect.schedules import IntervalSchedule
from prefect.storage import Docker
from prefect.tasks.gcp.storage import GCSUpload
from prefect.tasks.secrets import PrefectSecret

from scraping import scraper


@prefect.task
def get_reference_datetime(ref_datetime):
    ref_datetime = ref_datetime or prefect.context.get("scheduled_start_time")
    return arrow.get(ref_datetime)


@prefect.task
def scrap_from_datetime(ref_datetime: arrow.Arrow):
    query = scraper.QueryEnergyProduction(ref_datetime, live_query=True)
    return query.query_regional_production_live()


@prefect.task
def make_records_dump(records: list):
    return json.dumps(records)


@prefect.task
def get_upload_blob(ref_datetime: arrow.Arrow):
    return ref_datetime.format(fmt="YYYY/MM/DD/HH-mm-ss") + ".json"


@prefect.task
def parse_records(records_to_parse):
    return list(scraper.parse_response(records_to_parse, on_keyerror="warn"))


@prefect.task
def push_to_pubsub(records, credentials):
    project_id = "rte-eco2mix-regional"
    subject_id = "regional_records"
    credentials = Credentials.from_service_account_info(credentials)

    publisher = pubsub_v1.PublisherClient(credentials=credentials)
    topic_path = publisher.topic_path(project_id, subject_id)

    for record in records:
        encoded_record = json.dumps(record).encode("utf-8")
        publisher.publish(topic_path, encoded_record)


retrieve_gcp_credentials = PrefectSecret("GCP_CREDENTIALS")
upload_raw_records = GCSUpload(bucket="rte_scraping_results")


scheduler = IntervalSchedule(interval=timedelta(minutes=60))

run_config = DockerRun(labels=["staging"])
storage = Docker(
    registry_url="loicmac", image_name="rte-eco2mix", dockerfile="Dockerfile"
)

with prefect.Flow(
    "regional_data",
    run_config=run_config,
    storage=storage,
    schedule=scheduler,
) as flow:
    gcp_credentials = retrieve_gcp_credentials()
    datetime_param = DateTimeParameter("reference_datetime", required=False)
    reference_datetime = get_reference_datetime(datetime_param)
    records = scrap_from_datetime(reference_datetime)
    save_blob = get_upload_blob(reference_datetime)
    records_dump = make_records_dump(records)
    upload_raw_records(records_dump, credentials=gcp_credentials, blob=save_blob)
    parsed_records = parse_records(records)
    push_to_pubsub(parsed_records, gcp_credentials)
