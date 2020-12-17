from dotenv import load_dotenv
import pytest

from db_schema.dal import DAL
from db_schema import RegionalEnergyProduction
from save_parse_results import save_to_db

load_dotenv("database_test.env", verbose=True)

dal = DAL.from_env()


@pytest.fixture(autouse=True)
def cleanup_test_db():
    delete_regional_energy_production_records()
    yield
    delete_regional_energy_production_records()


def delete_regional_energy_production_records():
    with dal.session_scope() as session:
        session.query(RegionalEnergyProduction).delete()


def test_save_to_db():
    record_to_save = {
        "region_code": 25,
        "region": "Bourgogne-Franche-Comté",
        "dataset_id": "eco2mix-regional-tr",
        "record_id": "a999adgt",
        "datetime": "2020-12-15T17:30:00",
        "total_consumption": 1132.0,
        "production": {"ech_physiques": 1132.0, "nucleaire": None},
        "flux": {"flux_physiques_de_bourgogne_franche_comte_vers_grand_est": 1132.0},
    }

    save_to_db([record_to_save], dal)

    assert count_records() == 1
    expected_orm_object = RegionalEnergyProduction.from_parsed_record(record_to_save)
    with dal.session_scope() as session:
        res = session.query(RegionalEnergyProduction).first()
        res == expected_orm_object


def count_records():
    with dal.session_scope() as session:
        return session.query(RegionalEnergyProduction).count()
