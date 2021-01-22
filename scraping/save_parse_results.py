import logging

from db_schema import RegionalEnergyProduction

logger = logging.getLogger(__name__)


def save_to_db(parsed_records, dal):
    with dal.session_scope() as session:
        objects_to_insert = [
            RegionalEnergyProduction.from_parsed_record(record)
            for record in parsed_records
        ]
        logger.info(f"Saving {len(objects_to_insert)} objects to db")
        session.bulk_save_objects(objects_to_insert)
