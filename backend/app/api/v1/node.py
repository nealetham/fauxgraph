from fastapi import APIRouter, HTTPException, Request
from uuid import UUID
from app.models.schemas import Node
from app.services.session import SessionService

router = APIRouter(prefix="/nodes", tags=["nodes"])

@router.post("/", response_model=Node)
async def create_node(node: Node, request: Request):
    session = SessionService.get_session_graph(request)

    node_dict = node.model_dump()
    node_dict["id"] = SessionService.serialize_uuid(node.id)

    session["nodes"][node_dict["id"]] = node_dict
    return node

@router.get("/", response_model=list[Node])
async def get_nodes(request: Request):
    session = SessionService.get_session_graph(request)
    return [
        SessionService.deserialize_node(node_dict)
        for node_dict in session["nodes"].values()
    ]

@router.get("/{node_id}", response_model=Node)
async def get_node(node_id: UUID, request: Request):
    session = SessionService.get_session_graph(request)
    node_str_id = SessionService.serialize_uuid(node_id)

    if node_str_id not in session["nodes"]:
        return HTTPException(status_code=404, detail="Node not found")
    
    return SessionService.deserialize_node(session["nodes"][node_str_id])
