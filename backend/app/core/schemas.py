from pydantic import BaseModel

class NodeSchema(BaseModel):
    name: str
    attributes: dict
    count: int

class EdgeSchema(BaseModel):
    source: str
    target: str
    relation: str
    probability: float

class GraphSchema(BaseModel):
    nodes: list[NodeSchema]
    edges: list[EdgeSchema]
