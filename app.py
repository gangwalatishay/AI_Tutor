from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent.executor import stream_video_agent

app = FastAPI()

class VideoRequest(BaseModel):
    goal: str

@app.post("/video-agent/stream")
def stream_agent(req: VideoRequest):
    return StreamingResponse(
        stream_video_agent(req.goal),
        media_type="text/event-stream"
    )
