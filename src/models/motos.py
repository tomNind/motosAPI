from sqlmodel import SQLModel, Field

class Moto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    marca: str
    modelo: str
    año: int
    nueva: bool



