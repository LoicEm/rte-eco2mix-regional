from sqlalchemy import Column, Integer, String, DateTime, JSON, Float

from db_schema.base import Base


class RegionalEnergyProduction(Base):

    __tablename__ = "regional_production"

    id = Column(Integer, primary_key=True)
    region_code = Column(String)
    region_string = Column(String)
    dataset_id = Column(String)
    record_id = Column(String)
    datetime = Column(DateTime)
    total_consumption = Column(Float)
    production = Column(JSON)
    flux = Column(JSON)

    @classmethod
    def from_parsed_record(cls, record):
        return cls(
            region_code=record["region_code"],
            region_string=record["region"],
            dataset_id=record["dataset_id"],
            record_id=record["record_id"],
            datetime=record["datetime"],
            total_consumption=record["total_consumption"],
            production=record["production"],
            flux=record["flux"],
        )
