from fastapi import APIRouter, HTTPException, Request
from uuid import UUID
from app.services.session import SessionService
from app.models.schemas import Edge

router = APIRouter(prefix="/edges", tags=["edges"])

@router.post("/", response_model=Edge)
async def add_edge(edge: Edge, request: Request):
    session = SessionService.get_session_graph(request)

    source_id = SessionService.serialize_uuid(edge.source_id)
    target_id = SessionService.serialize_uuid(edge.target_id)

    if source_id not in session["nodes"]:
        raise HTTPException(status_code=404, detail="Source node not found")
    if target_id not in session["nodes"]:
        raise HTTPException(status_code=404, detail="Target node not found")

    edge_dict = edge.model_dump()
    edge_dict["id"] = SessionService.serialize_uuid(edge.id)
    edge_dict["source_id"] = source_id
    edge_dict["target_id"] = target_id

    session["edges"][edge_dict["id"]] = edge_dict
    return edge

@router.get("/", response_model=list[Edge])
async def get_edges(request: Request):
    session = SessionService.get_session_graph(request)
    return [
        SessionService.deserialize_edge(edge_dict)
        for edge_dict in session["edges"].values()
    ]

@router.get("/{edge_id}", response_model=Edge)
async def get_edge(edge_id: UUID, request: Request):
    session = SessionService.get_session_graph(request)
    edge_str_id = SessionService.serialize_uuid(edge_id)

    if edge_str_id not in session["edges"]:
        return HTTPException(status_code=404, detail="Edge not found.")
    
    return SessionService.deserialize_edge(session["edges"][edge_str_id])
