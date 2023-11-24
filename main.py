from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de datos para una paciente
class Paciente(BaseModel):
    nombre: str
    edad: int
    cedula: str
    id: int
    city: str

# Lista para almacenar paciente (simulación de base de datos)
paciente_db = []

# Operación para crear una paciente
@app.post("/paciente/", response_model=Paciente)
def create_paciente(paciente: Paciente):
    paciente_db.append(paciente)
    return paciente

# Operación para obtener todas las paciente
@app.get("/paciente/", response_model=List[Paciente])
def get_all_paciente():
    return paciente_db

# Operación para obtener una paciente por ID
@app.get("/paciente/{paciente_id}", response_model=Paciente)
def get_paciente_by_id(paciente_id: int):
    for paciente in paciente_db:
        if paciente.id == paciente_id:
            return paciente
    raise HTTPException(status_code=404, detail="Paciente no encontrada")

# Operación para editar una paciente por ID
@app.put("/paciente/{paciente_id}", response_model=Paciente)
def update_paciente(paciente_id: int, updated_paciente: Paciente):
    for index, paciente in enumerate(paciente_db):
        if paciente.id == paciente_id:
            paciente_db[index] = updated_paciente
            return updated_paciente
    raise HTTPException(status_code=404, detail="Paciente no encontrada")

# Operación para eliminar una paciente por ID
@app.delete("/paciente/{paciente_id}", response_model=Paciente)
def delete_paciente(paciente_id: int):
    for index, paciente in enumerate(paciente_db):
        if paciente.id == paciente_id:
            deleted_paciente = paciente_db.pop(index)
            return deleted_paciente
    raise HTTPException(status_code=404, detail="Paciente no encontrada")
