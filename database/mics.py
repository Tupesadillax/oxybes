from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

engine = create_engine('sqlite:///database/database.db', echo = False)
# engine = create_engine('postgresql://oxybes:7105017829@localhost/lanamilana', echo = False)
metadata = Base.metadata
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()