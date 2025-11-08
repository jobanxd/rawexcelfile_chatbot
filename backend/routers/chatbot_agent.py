import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from chatbot_agent.agent import root_agent

from google.genai import types as genai_types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory import InMemoryMemoryService

from models.chatbot_agent import (
    ChatbotAgentRequest,
    ChatbotAgentResponse,
)

# Init services for Runner
session_svc = InMemorySessionService()
artifact_svc = InMemoryArtifactService()
memory_svc = InMemoryMemoryService()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate", response_model=ChatbotAgentResponse)
async def generate_respones(request: ChatbotAgentRequest):
    try:

        session = await session_svc.get_session(
            app_name="Chatbot Agent",
            user_id=request.user_id,
            session_id=request.session_id,
        )

        if session:
            logger.info("Found existing session. Using session ID: %s", request.session_id)

        if not session:
            session = await session_svc.create_session(
                app_name="Chatbot Agent",
                user_id=request.user_id,
                session_id=request.session_id,
                state={},
            )
            logger.info("Created new session. Using session ID: %s", request.session_id)

        runner = Runner(
            agent=root_agent,
            app_name="Chatbot Agent",
            session_service=session_svc,
            memory_service=memory_svc,
            artifact_service=artifact_svc,
        )

        user_content = genai_types.Content(
            role="user",
            parts=[genai_types.Part(text=request.input_query)]
        )

        events = runner.run_async(
            user_id=request.user_id,
            session_id=request.session_id,
            new_message=user_content,
        )

        response_parts=[]

        async for event in events:
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text and not part.thought:
                            response_parts.append(part.text)
        
        response_message = "".join(response_parts).strip()
        logger.info("Response Message: %s", response_message)
        
        return ChatbotAgentResponse(
            response=response_message,
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

    