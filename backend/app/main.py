from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

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
    interests: List[str] = Field(default_factory=lambda: ["naturaleza"])

@app.get("/")
def root():
    return {"message": "OPITA 360 API está funcionando", "docs": "/docs"}

@app.get("/api/destinations")
def list_destinations():
    return {"destinations": DESTINATIONS, "total": len(DESTINATIONS)}

@app.post("/api/recommendations")
def recommend_trip(request: TripRequest):
    selected = [d for d in DESTINATIONS if any(
        interest.lower() in [tag.lower() for tag in d["tags"]] or
        interest.lower() == d["category"].lower()
        for interest in request.interests
    )]
    if not selected:
        selected = DESTINATIONS[:]
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
    return {
        "summary": f"Propuesta de {len(itinerary)} parada(s) para {request.days} día(s).",
        "method": "Recomendación basada en reglas: intereses, duración y presupuesto.",
        "itinerary": itinerary,
        "estimated_total": total,
        "budget": request.budget,
        "remaining_budget": remaining,
        "notice": "Valores orientativos para demostración; confirma precios, horarios y transporte antes de viajar."
    }
