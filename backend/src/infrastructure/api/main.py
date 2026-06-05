import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.dtos.schemas import MorphismRequest, MorphismResponse
from src.adapters.controllers.morphism_controller import MorphismController

app = FastAPI(title="MorphFinder API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/v1/morphisms/find", response_model=MorphismResponse)
async def find_morphisms(request: MorphismRequest):
    try:
        # Delegate to the Interface Adapter (Controller)
        controller = MorphismController()
        return controller.find_morphisms(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
