from unittest.mock import patch

import arrow
import pytest

import scraper


def test_get_datetime_query_params():
    end_datetime = arrow.get("2020-11-12T22:05:47")
    result = scraper.get_datetime_query_param(end_datetime)
    assert result == "date_heure:[2020-11-11T22:05 TO 2020-11-12T22:05]"


@pytest.mark.parametrize(
    "live_query, expected_dataset",
    [
        (True, {"dataset": scraper.LIVE_DATASET}),
        (False, {"dataset": scraper.CONSOLIDATED_DATASET}),
    ],
)
def test_get_query_params(live_query, expected_dataset):
    tested_query = scraper.QueryEnergyProduction(
        arrow.get("2020-11-12T22:05:47"), live_query=live_query
    )
    expected_params = dict(
        {"q": "date_heure:[2020-11-11T22:05 TO 2020-11-12T22:05]", "rows": 0},
        **expected_dataset
    )
    assert tested_query.get_query_params(n_rows=0) == expected_params


@patch("scraper.RecordParser")
def test_parse_response_yields_one_result_per_record(mock_parser):
    response_to_parse = {"nhits": 1000, "parameters": {}, "records": [1] * 1000}
    assert len([res for res in scraper.parse_response(response_to_parse)]) == 1000


def test_parse_record():
    record_to_parse = {
        "datasetid": "test_dataset",
        "recordid": "f1c10a15c2a4eb840818d81738d30f0c57ee75ad",
        "fields": {
            "libelle_region": "Centre-Val de Loire",
            "tch_bioenergies": 60,
            "eolien": 200,
            "hydraulique": 0,
            "flux_physiques_de_grand_est_vers_centre_val_de_loire": "-",
            "solaire": 0,
            "ech_physiques": -1,
            "tco_thermique": 2.63,
            "nucleaire": 1000,
            "code_insee_region": "24",
            "thermique": 5,
            "bioenergies": 30,
            "date_heure": "2020-12-07T17:30:00+00:00",
            "consommation": 1234,
        },
        "record_timestamp": "2020-12-08T16:03:18.317000+00:00",
    }
    expected_result = {
        "region_code": "24",
        "region": "Centre-Val de Loire",
        "dataset_id": "test_dataset",
        "record_id": "f1c10a15c2a4eb840818d81738d30f0c57ee75ad",
        "datetime": "2020-12-07T17:30:00+00:00",
        "total_consumption": 1234,
        "production": {
            "nucleaire": 1000,
            "eolien": 200,
            "bioenergies": 30,
            "thermique": 5,
            "solaire": 0,
            "hydraulique": 0,
            "pompage": 0,
            "ech_physiques": -1,
        },
        "flux": {"flux_physiques_de_grand_est_vers_centre_val_de_loire": 0},
    }

    parser = scraper.RecordParser(
        record_to_parse, config_path=scraper.RECORDS_PARSING_CONFIG
    )
    assert parser.parse() == expected_result
