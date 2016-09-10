from Database.models import Base
import tables
from models import engine
Base.metadata.create_all(engine)