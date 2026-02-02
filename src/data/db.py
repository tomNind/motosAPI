from sqlmodel import create_engine, SQLModel, Session, select, func
from src.models.motos import Moto
import os

# Credenciales de MySQL en Docker
db_user: str = "quevedo"
db_password: str = "1234"
db_server: str = "fastapi-db"   
db_port: int = 5432
db_name: str = "motosdb"

# URL de conexión
DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"

# Crear engine
engine = create_engine(os.getenv("DB_URL", DATABASE_URL), echo=True)

# Sesión
def get_session():
    with Session(engine) as session:
        yield session

# Nuevo id

def get_next_id(session):
    max_id = session.exec(select(func.max(Moto.id))).one()
    if max_id is None:
        return 1
    return max_id + 1

# Inicializar base de datos con datos de ejemplo
def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(Moto(id=1, marca="Yamaha", modelo="MT-07", año=2020, nueva=True))
        session.add(Moto(id=2, marca="Honda", modelo="CB500F", año=2019, nueva=False))
        session.add(Moto(id=3, marca="Kawasaki", modelo="Z900", año=2021, nueva=True))
        session.add(Moto(id=4, marca="BMW", modelo="R1250GS", año=2018, nueva=False))
        session.add(Moto(id=5, marca="Ducati", modelo="Monster", año=2022, nueva=True))
        session.commit()



