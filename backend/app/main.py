from fastapi import FastAPI
import faker
import random
import networkx as nx
import pandas as pd
from core.schemas import GraphSchema

app = FastAPI()
fake = faker.Faker()

@app.post("/generate/")
def generate_graph(schema: GraphSchema):
    G = create_graph(schema)
    data = nx.node_link_data(G)  # Converts to JSON
    return {"graph": data}

@app.post("/export/csv/")
def export_csv(schema: GraphSchema):
    G = create_graph(schema)
    node_df = pd.DataFrame([{"id": n, **G.nodes[n]} for n in G.nodes])
    edge_df = pd.DataFrame([(s, t, G[s][t]["relation"]) for s, t in G.edges], columns=["source", "target", "relation"])
    
    node_csv = node_df.to_csv(index=False)
    edge_csv = edge_df.to_csv(index=False)
    
    return {"nodes_csv": node_csv, "edges_csv": edge_csv}

def generate_fake_value(value_type):
    if value_type == "str":
        return fake.name()
    elif value_type == "int":
        return random.randint(18, 60)
    elif value_type == "email":
        return fake.email()
    return None

def create_graph(schema: GraphSchema):
    G = nx.Graph()
    node_data = {}

    # Generate nodes
    for node in schema.nodes:
        for i in range(node.count):
            node_id = f"{node.name}_{i}"
            attributes = {attr: generate_fake_value(node.attributes[attr]) for attr in node.attributes}
            G.add_node(node_id, **attributes)
            node_data.setdefault(node.name, []).append(node_id)

    # Generate edges
    for edge in schema.edges:
        for src in node_data.get(edge.source, []):
            for tgt in node_data.get(edge.target, []):
                if src != tgt and random.random() < edge.probability:
                    G.add_edge(src, tgt, relation=edge.relation)

    return G
