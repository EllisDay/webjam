import os
import math
from typing import Dict, List, Optional, Tuple

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

# ------------------------------
# Config (env vars)
# ------------------------------
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY") or os.getenv("GOOGLE_MAPS_API_KEY", "")
CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "http://127.0.0.1:5500,http://localhost:5500,http://localhost:5173").split(",")

DEFAULT_RADIUS_METERS = int(os.getenv("PLACES_RADIUS_METERS", "30000"))  # 30km ~ 18.6 miles
MAX_RESULTS = int(os.getenv("PLACES_MAX_RESULTS", "25"))  # frontend shows 25

# ------------------------------
# App
# ------------------------------
app = FastAPI(title="MediCheck Backend (Places API v1)", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Helpers
# ------------------------------
def haversine_miles(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    R = 3958.8
    (lat1, lon1), (lat2, lon2) = (map(math.radians, a), map(math.radians, b))
    dlat, dlon = (lat2 - lat1, lon2 - lon1)
    h = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return 2 * R * math.asin(min(1.0, math.sqrt(h)))

async def geocode_address(query: str) -> Optional[Dict]:
    """Use Geocoding API once to turn q (city/ZIP) into lat/lng."""
    if not GOOGLE_PLACES_API_KEY:
        raise HTTPException(500, "Server missing GOOGLE_PLACES_API_KEY/GOOGLE_MAPS_API_KEY")
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": query, "key": GOOGLE_PLACES_API_KEY}
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
    if not data.get("results"):
        return None
    top = data["results"][0]
    loc = top["geometry"]["location"]
    return {"lat": loc["lat"], "lng": loc["lng"], "formatted": top.get("formatted_address")}

async def places_search_nearby(lat: float, lng: float, radius_m: int, max_results: int = 20) -> List[Dict]:
    """
    Google Places API (New) v1 nearby search.
    POST https://places.googleapis.com/v1/places:searchNearby
    Headers: X-Goog-Api-Key, X-Goog-FieldMask
    Body: includedTypes, locationRestriction.circle, maxResultCount
    """
    if not GOOGLE_PLACES_API_KEY:
        raise HTTPException(500, "Server missing GOOGLE_PLACES_API_KEY/GOOGLE_MAPS_API_KEY")

    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
        # Ask only for fields we need
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.location",
    }
    payload = {
        "includedTypes": ["hospital"],
        "maxResultCount": min(max_results, 20),  # v1 caps per page ~20
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": radius_m
            }
        }
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(url, headers=headers, json=payload)
        if r.status_code >= 400:
            # Bubble up the API’s error to help debugging
            try:
                detail = r.json()
            except Exception:
                detail = r.text
            raise HTTPException(status_code=502, detail=f"Places error: {detail}")
        data = r.json()

    return data.get("places", []) or []


# ------------------------------
# Endpoints
# ------------------------------

@app.get("/api/nearby")
async def api_nearby(
    q: str = Query(..., description="City or ZIP"),
    limit: int = Query(MAX_RESULTS, ge=1, le=100),
    radius_meters: int = Query(DEFAULT_RADIUS_METERS, ge=1000, le=80000),  # clamp 1–80km
):
    """
    Returns closest hospitals near the provided city/ZIP using Places API (New).
    {
      origin: {lat,lng,formatted},
      count, results: [{name,formatted,lat,lng,distance}]
    }
    """
    origin = await geocode_address(q)
    if not origin:
        raise HTTPException(404, "Location not found")

    places = await places_search_nearby(origin["lat"], origin["lng"], radius_meters, max_results=min(limit, 20))

    results: List[Dict] = []
    for p in places:
        name = (p.get("displayName") or {}).get("text") or "Unknown"
        loc = (p.get("location") or {})
        plat, plng = loc.get("latitude"), loc.get("longitude")
        if plat is None or plng is None:
            continue
        distance = haversine_miles((origin["lat"], origin["lng"]), (plat, plng))
        results.append({
            "name": name,
            "formatted": p.get("formattedAddress"),
            "lat": plat,
            "lng": plng,
            "distance": distance,
        })

    # Sort by distance (Places tends to return nearby already, but we ensure order)
    results.sort(key=lambda r: r["distance"])
    # If you want more than 20 results, you can add paging with nextPageToken (not shown here)
    results = results[:limit]

    return {
        "origin": origin,
        "count": len(results),
        "results": results,
    }

@app.get("/api/health")
async def api_health():
    return {"ok": True}
