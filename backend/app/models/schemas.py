from pydantic import BaseModel, Field
from typing import Any
from uuid import UUID, uuid4

class Node(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    label: str
    attributes: dict[str, Any] = Field(default_factory=dict)
    count: int

class Edge(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    source_id: UUID
    target_id: UUID
    type: str
    probability: float

class GraphSchema(BaseModel):
    nodes: list[Node]
    edges: list[Edge]
