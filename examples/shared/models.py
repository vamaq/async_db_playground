from sqlalchemy import Column
from sqlalchemy.types import DateTime, Integer, Float, String, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

metadata_schema = declarative_base()


class MagicProjectMirror(metadata_schema):
    """ Target table to mirror content of magic_project """

    __tablename__ = 'magic_project_mirror'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    description = Column(String)
    finished = Column(Boolean)
    budget = Column(Float)
    duration_days = Column(Integer)
    resources = Column(ARRAY(String))
    created_at = Column(DateTime)
    insert_date = Column(DateTime)

