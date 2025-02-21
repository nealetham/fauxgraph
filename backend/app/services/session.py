from starlette.requests import Request
from uuid import UUID
from app.models.schemas import Node, Edge

class SessionService:

    @staticmethod
    def get_session_graph(request: Request):
        if "nodes" not in request.session:
            request.session["nodes"] = {}
        if "edges" not in request.session:
            request.session["edges"] = {}
        return request.session

    @staticmethod
    def serialize_uuid(uuid: UUID) -> str:
        return str(uuid)
    
    @staticmethod
    def deserialize_node(node_dict: dict) -> Node:
        return Node(
            id=UUID(node_dict["id"]),
            label=node_dict["label"],
            attributes = node_dict["attributes"],
            count= node_dict["count"]
        )
    
    @staticmethod
    def deserialize_edge(edge_dict: dict) -> Edge:
        return Edge(
            id=UUID(edge_dict["id"]),
            type=edge_dict["type"],
            source_id=UUID(edge_dict["source_id"]),
            target_id=UUID(edge_dict["target_id"]),
            properties=edge_dict["probability"]
        )
