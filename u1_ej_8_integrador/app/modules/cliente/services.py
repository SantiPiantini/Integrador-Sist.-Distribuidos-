from typing import List, Optional
from .schemas import ClienteCreate, ClienteRead
from ..producto.services import id_counter

db_clientes: List[ClienteRead] = [
    ClienteRead(id=1, nombre="Ana Garcia", email="anagarcia12@gmail.com", telefono="+5491234567890", activo=True),
    ClienteRead(id=2, nombre="Pablo Sanchez", email="pablitosanchezcabj@gmail.com", telefono="+5491234512120", activo=True),
]
id_counter = 3

def crear(data: ClienteCreate) -> ClienteRead:
    global id_counter
    if obtener_por_email(data.email):
        raise ValueError(f"Ya existe un cliente con el mail: {data.email}")
    nuevo = ClienteRead(id=id_counter, **data.model_dump())
    db_clientes.append(nuevo)
    id_counter += 1
    return nuevo

def obtener_todos(skip: int = 0, limit: int = 10) -> List[ClienteRead]:
    return db_clientes[skip:skip + limit]

def obtener_por_id(id: int) -> Optional[ClienteRead]:
    for c in db_clientes:
        if c.id == id:
            return c
    return None

def obtener_por_email(email: str) -> Optional[ClienteRead]:
    for c in db_clientes:
        if c.email == email.lower():
            return c
    return None

def buscar(nombre: Optional[str], activo: Optional[bool]) -> Optional[ClienteRead]:
    resultado = db_clientes
    if nombre:
        resultado = [c for c in resultado if nombre.lower() in c.nombre.lower()]
    if activo is not None:
        resultado = [c for c in resultado if c.activo == activo]
    return resultado

def actualizar_total(id: int, data: ClienteCreate) -> Optional[ClienteRead]:
    for index, c in enumerate(db_clientes):
        if c.id == id:
            existente = obtener_por_email(data.email)
            if existente and existente.id != id:
                raise ValueError(f"El email '{data.email}' ya esta en uso por otro cliente")
            actualizado = ClienteRead(id=id, **data.model_dump())
            db_clientes[index] = actualizado
            return actualizado
    return None

def desactivar (id: int) -> Optional[ClienteRead]:
    for index, c in enumerate(db_clientes):
        if c.id == id:
            c_dict = c.model_dump()
            c_dict["activo"] = False
            actualizado = ClienteRead(**c_dict)
            db_clientes[index] = actualizado
            return actualizado
    return None

def obtener_estado(id: int) -> Optional[dict]:
    cliente = obtener_por_id(id)
    if not cliente:
        return None
    mensaje = "Cliente activo y habilitado para operar" if cliente.activo else "Cliente desactivado, no puede operar"
    return {"id": cliente.id, "nombre": cliente.nombre, "activo":cliente.activo, "mensaje": mensaje}