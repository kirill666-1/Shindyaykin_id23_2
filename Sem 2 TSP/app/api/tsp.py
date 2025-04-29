from fastapi import APIRouter, Depends, HTTPException
from app.schemas.tsp import Graph, PathResult
from app.services.tsp import nearest_neighbor_tsp
from app.core.security import decode_access_token
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter()

@router.post("/shortest-path/", response_model=PathResult)
def shortest_path(graph: Graph, token: str = Depends(lambda x: x.headers.get("Authorization").split(" ")[1]), db: Session = Depends(get_db)):
    try:
        decode_access_token(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    try:
        path, total_distance = nearest_neighbor_tsp(graph.nodes, graph.edges)
        return {"path": path, "total_distance": total_distance}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))