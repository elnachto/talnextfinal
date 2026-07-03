from core.database import Base, engine
from models.user import User
from models.interview_record import InterviewRecord
from models.comparison import Comparison


def init_database():
    print("Creando tablas en la base de datos (por favor funciona)")
    Base.metadata.create_all(bind=engine)
    print("La cosita esta funcionó MAS BIEN.")


if __name__ == "__main__":
    init_database()