from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import Optional, List
from . import schemas, services

router = APIRouter(prefix="/cliente", tags=["cliente"])

@router.post("/", response_model=schemas.ClienteRead, status_code=status.HTTP_201_CREATED)
def alta_cliente(cliente: schemas.ClienteCreate):
    try:
        return services.crear(cliente)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@router.get("/", response_model=List[schemas.ClienteRead], status_code=status.HTTP_200_OK)
def listar_clientes(
    nombre: Optional[str] = Query(None, description="Filtrar por nombre (parcial)"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
):
    resultados = services.buscar(nombre, activo)
    return resultados[skip: skip + limit]


@router.get("/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK)
def detalle_cliente(id: int = Path(..., gt=0)):
    cliente = services.obtener_por_id(id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente


@router.put("/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK)
def actualizar_cliente(cliente: schemas.ClienteCreate, id: int = Path(..., gt=0)):
    try:
        actualizado = services.actualizar_total(id, cliente)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    if not actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return actualizado


@router.put("/{id}/desactivar", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK)
def borrado_logico(id: int = Path(..., gt=0)):
    desactivado = services.desactivar(id)
    if not desactivado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return desactivado


@router.get("/{id}/estado", response_model=schemas.ClienteEstadoResponse, status_code=status.HTTP_200_OK)
def estado_cliente(id: int = Path(..., gt=0)):
    resultado = services.obtener_estado(id)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return resultado