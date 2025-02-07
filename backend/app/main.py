from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.websocket import GestureWebSocket

app = FastAPI(title=settings.PROJECT_NAME)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize WebSocket manager
gesture_ws = GestureWebSocket()

@app.websocket("/ws/gesture")
async def websocket_endpoint(websocket: WebSocket):
    await gesture_ws.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await gesture_ws.process_frame(websocket, data)
    except Exception as e:
        print(f"Error: {e}")
        if websocket in gesture_ws.active_connections:
            gesture_ws.disconnect(websocket)

@app.get("/")
async def root():
    return {"message": "Gesture Recognition API"}