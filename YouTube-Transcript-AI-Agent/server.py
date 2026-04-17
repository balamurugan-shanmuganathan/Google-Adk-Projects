import os
import sys
import asyncio

# Ensure dependencies from the venv are accessible
venv_path = os.path.abspath(os.path.join(os.getcwd(), "..", ".venv", "lib", "python3.9", "site-packages"))
if venv_path not in sys.path:
    sys.path.append(venv_path)

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from youtube_transcript_ai_agent.agent import root_agent
from google.genai import types
from google.adk.agents.run_config import RunConfig, StreamingMode

app = FastAPI(title="YouTube Transcript AI Agent UI Server")

# Initialize Runner
# Using InMemorySessionService for the web UI simplicity
session_service = InMemorySessionService()
runner = Runner(
    app_name="YouTube-Transcript-UI",
    agent=root_agent,
    session_service=session_service
)

# Constants for UI
USER_ID = "WebUser"
SESSION_ID = "WebSession"

@app.on_event("startup")
async def startup_event():
    # Ensure session exists
    await session_service.create_session(
        app_name="YouTube-Transcript-UI",
        user_id=USER_ID,
        session_id=SESSION_ID
    )

@app.get("/stream")
async def stream_agent_output(url: str = Query(..., description="The YouTube URL to process")):
    async def event_generator():
        new_message = types.Content(
            role="user",
            parts=[types.Part(text=f"Please analyze this YouTube video: {url}")]
        )
        
        # SSE streaming mode
        run_config = RunConfig(streaming_mode=StreamingMode.SSE)
        
        try:
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=SESSION_ID,
                new_message=new_message,
                run_config=run_config,
            ):
                # Extremely strict filter
                # We only want the AI's generated response, not tool outputs or intermediate text
                if event.content and event.content.parts and event.agent_name == root_agent.name:
                    # In some versions of ADK, tool outputs might have a different agent name or type
                    # We ensure we're getting fresh text chunks
                    chunk = "".join(p.text for p in event.content.parts if p.text)
                    if chunk:
                        yield chunk
            
            # End signal
            yield "[DONE]"
        except Exception as e:
            print(f"Error in agent stream: {e}")
            yield f"Error: {str(e)}"

    return EventSourceResponse(event_generator())

# Serve static files AFTER defining routes
app.mount("/", StaticFiles(directory="ui", html=True), name="ui")

if __name__ == "__main__":
    import uvicorn
    # Running on 8001 as 8000 might be in use
    print("Starting Premium UI Server on http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
