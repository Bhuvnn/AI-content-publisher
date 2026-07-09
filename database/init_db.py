from database.database import Base, engine

# Import all models so SQLAlchemy knows about them
from database.models import Poem


def init_db():
    Base.metadata.create_all(bind=engine)
