from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Recording(Base):
    __tablename__ = 'recordings'
    id:int = Column(Integer, primary_key=True)
    project:str = Column(String(120), unique=False)
    name:str = Column(String(120), unique=True)
    path:str = Column(String(120), unique=True)
    upload:bool = Column(Boolean, unique=False, default=False)
    uploaded:bool = Column(Boolean, unique=False, default=False)

    def __init__(self, project=None, name=None, path=None):
        self.project = project
        self.name = name
        self.path = path
    