from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, StrictStr, StringConstraints
from typing import Annotated, List, Optional

# El catálogo de demostración del frontend (frontend/src/fallback-destinations.json)
# debe ser idéntico a DESTINATIONS; backend/tests/test_review_fixes.py lo verifica.
Interest = Annotated[str, StringConstraints(strip_whitespace=True, max_length=40)]

app = FastAPI(
    title="OPITA 360 API",
    version="1.0.0",
    description="API de destinos y recomendaciones turísticas para el Huila."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DESTINATIONS = [
    {
        "id": 1, "name": "Desierto de la Tatacoa", "municipality": "Villavieja",
        "category": "Naturaleza", "price": 85000, "days": 1,
        "description": "Paisajes rojizos, senderos y observación del cielo nocturno.",
        "emoji": "🌵", "tags": ["naturaleza", "aventura", "fotografía", "astronomía"],
        "color": "sand"
    },
    {
        "id": 2, "name": "Parque Arqueológico de San Agustín", "municipality": "San Agustín",
        "category": "Cultura", "price": 120000, "days": 1,
        "description": "Estatuas ancestrales, historia y patrimonio arqueológico.",
        "emoji": "🗿", "tags": ["cultura", "historia", "familia", "arqueología"],
        "color": "green"
    },
    {
        "id": 3, "name": "Malecón del río Magdalena", "municipality": "Neiva",
        "category": "Cultura", "price": 35000, "days": 1,
        "description": "Un recorrido urbano para disfrutar el río y la identidad opita.",
        "emoji": "🌅", "tags": ["cultura", "gastronomía", "familia", "relajación"],
        "color": "blue"
    },
    {
        "id": 4, "name": "Salto de Bordones", "municipality": "Isnos",
        "category": "Naturaleza", "price": 95000, "days": 1,
        "description": "Una imponente caída de agua rodeada de montañas y vegetación.",
        "emoji": "💧", "tags": ["naturaleza", "aventura", "fotografía", "senderismo"],
        "color": "blue"
    },
    {
        "id": 5, "name": "Estrecho del río Magdalena", "municipality": "San Agustín",
        "category": "Aventura", "price": 70000, "days": 1,
        "description": "Un tramo singular del río entre grandes formaciones rocosas.",
        "emoji": "🏞️", "tags": ["aventura", "naturaleza", "fotografía", "senderismo"],
        "color": "green"
    },
    {
        "id": 6, "name": "Termales de Rivera", "municipality": "Rivera",
        "category": "Bienestar", "price": 65000, "days": 1,
        "description": "Aguas termales y descanso en un entorno natural.",
        "emoji": "♨️", "tags": ["relajación", "naturaleza", "familia", "bienestar"],
        "color": "sand"
    },
    {
        "id": 7, "name": "Represa de Betania", "municipality": "Yaguará",
        "category": "Aventura", "price": 90000, "days": 1,
        "description": "Paisajes acuáticos y actividades recreativas según disponibilidad local.",
        "emoji": "🛶", "tags": ["aventura", "naturaleza", "familia", "fotografía"],
        "color": "blue"
    },
    {
        "id": 8, "name": "Centro de Neiva y tradición opita", "municipality": "Neiva",
        "category": "Cultura", "price": 45000, "days": 1,
        "description": "Sabores regionales, espacios culturales y tradición del Huila.",
        "emoji": "🎭", "tags": ["cultura", "gastronomía", "historia", "familia"],
        "color": "sand"
    }
]

class TripRequest(BaseModel):
    days: int = Field(default=2, ge=1, le=14)
    budget: int = Field(default=200000, ge=0, le=100000000)
    interests: List[Interest] = Field(default_factory=lambda: ["naturaleza"], max_length=20)
    municipality: Optional[StrictStr] = Field(default=None, max_length=100)

@app.get("/")
def root():
    return {"message": "OPITA 360 API está funcionando", "docs": "/docs"}

@app.get("/api/destinations")
def list_destinations():
    return {"destinations": DESTINATIONS, "total": len(DESTINATIONS)}

@app.get("/api/destinations/{destination_id}")
def destination_detail(destination_id: int = Path(gt=0)):
    for destination in DESTINATIONS:
        if destination["id"] == destination_id:
            return {"destination": destination}
    raise HTTPException(status_code=404, detail="Destino no encontrado")


@app.post("/api/recommendations")
def recommend_trip(request: TripRequest):
    municipality = request.municipality.strip().casefold() if request.municipality else ""
    candidates = [d for d in DESTINATIONS if not municipality or d["municipality"].casefold() == municipality]
    selected = [d for d in candidates if any(
        interest.lower() in [tag.lower() for tag in d["tags"]] or
        interest.lower() == d["category"].lower()
        for interest in request.interests
    )]
    if not selected:
        selected = candidates[:]
    # Prioriza sitios asequibles y ajusta el número a los días solicitados.
    selected.sort(key=lambda d: (d["price"] > request.budget, d["price"]))
    itinerary, total = [], 0
    for destination in selected:
        if len(itinerary) >= request.days:
            break
        if total + destination["price"] <= request.budget or not itinerary:
            itinerary.append(destination)
            total += destination["price"]
    remaining = max(request.budget - total, 0)
    warnings = ""
    if total > request.budget:
        warnings += "La primera parada supera tu presupuesto; se incluye como referencia. "
    if itinerary and len(itinerary) < request.days:
        warnings += f"Solo hay {len(itinerary)} parada(s) para {request.days} día(s) con estos filtros. "
    return {
        "summary": f"Propuesta de {len(itinerary)} parada(s) para {request.days} día(s).",
        "method": "Recomendación basada en reglas: intereses, duración y presupuesto.",
        "itinerary": itinerary,
        "estimated_total": total,
        "budget": request.budget,
        "remaining_budget": remaining,
        "notice": ("No hay destinos disponibles para el municipio seleccionado. " if municipality and not candidates else "") + warnings + "Valores orientativos para demostración; confirma precios, horarios y transporte antes de viajar."
    }
