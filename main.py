from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
#importar librerias para el manejo de la base de datos pymongo
import pymongo
#libreria para generar un id unico
import uuid

#configuracion de mongo
cliente = pymongo.MongoClient("mongodb+srv://DanielMP84:WilmerMoreira@cluster0.mtqai5m.mongodb.net/?retryWrites=true&w=majority")
database = cliente["Pacientes"]
coleccion = database["Pacientes"]

app = FastAPI(
    title="API de pacientes",
    description="API para el manejo de pacientes de la clinica",
    version="1.0.1",
    contact={
        "name": "Daniel Moreira",
        "email": "wdmoreira3@utpl.edu.ec",
        "url": "https://github.com/Danielmp84/Utpl.Interoperabilidad.Api.2023"
    },
    license_info={
        "name": "MIT License",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    openapi_tags=[
        {
            "name": "Pacientes",
            "description": "Operaciones para el manejo de pacientes"
        }
    ]
)

# Modelo de datos para una paciente
class Paciente(BaseModel):
    nombre: str
    edad: int
    cedula: str
    city: str
    Cie10: str
    seguro: str
    direccion: str
    observacion: str

# Modelo de repositorio para un paciente
class PacienteRepositorio(BaseModel):
    nombre: str
    edad: int
    cedula: str
    id: str
    city: str
    Cie10: str
    seguro: str
    direccion: str
    observacion: str

# Lista para almacenar paciente (simulación de base de datos)
paciente_db = []

# Operación para crear una paciente
@app.post("/paciente/", response_model=PacienteRepositorio,tags=["Pacientes"])
def create_paciente(paciente: Paciente):
    idPaciente = str(uuid.uuid4())
    itemPaciente = PacienteRepositorio(nombre=paciente.nombre, edad=paciente.edad, cedula=paciente.cedula, city=paciente.city, id=idPaciente,direccion=paciente.direccion, seguro=paciente.seguro, Cie10=paciente.Cie10, observacion=paciente.observacion)   
    result = coleccion.insert_one(itemPaciente.dict())
    return itemPaciente

# Operación para obtener todas las paciente
@app.get("/paciente/", response_model=List[Paciente],tags=["Pacientes"])
def get_all_paciente():
    return paciente_db

# Operación para obtener una paciente por ID
@app.get("/paciente/{paciente_id}", response_model=Paciente,tags=["Pacientes"])
def get_paciente_by_id(paciente_id: int):
    for paciente in paciente_db:
        if paciente.id == paciente_id:
            return paciente
    raise HTTPException(status_code=404, detail="Paciente no encontrada")

# Operación para editar una paciente por ID
@app.put("/paciente/{paciente_id}", response_model=Paciente,tags=["Pacientes"])
def update_paciente(paciente_id: int, updated_paciente: Paciente):
    for index, paciente in enumerate(paciente_db):
        if paciente.id == paciente_id:
            paciente_db[index] = updated_paciente
            return updated_paciente
    raise HTTPException(status_code=404, detail="Paciente no encontrada")

# Operación para eliminar una paciente por ID
@app.delete("/paciente/{paciente_id}", response_model=Paciente,tags=["Pacientes"])
def delete_paciente(paciente_id: int):
    for index, paciente in enumerate(paciente_db):
        if paciente.id == paciente_id:
            deleted_paciente = paciente_db.pop(index)
            return deleted_paciente
    raise HTTPException(status_code=404, detail="Paciente no encontrada")
