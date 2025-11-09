import logging
from google.genai import types as genai_types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory import InMemoryMemoryService
from chatbot_agent.agent import root_agent
from core.settings import settings
from utils.logging_utils import boxed_log

# Initialize in-memory servicces
session_svc = InMemorySessionService()
artifact_svc = InMemoryArtifactService()
memory_svc = InMemoryMemoryService()

logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self):
        self.runner = Runner(
            agent=root_agent,
            app_name=settings.APP_NAME,
            session_service=session_svc,
            artifact_service=artifact_svc,
            memory_service=memory_svc,
        )

    async def generate_response(self, session_id: str, user_id: str, input_query: str) -> str:
        session = await session_svc.get_session(
            app_name=settings.APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )
        if session:
            logger.info("Found existing session. Using session ID: %s", session_id)
        else:
            session = await session_svc.create_session(
                app_name=settings.APP_NAME,
                user_id=user_id,
                session_id=session_id,
            )
            logger.info("Created new session. Using session ID: %s", session_id)
        
        user_content = genai_types.Content(
            role="user",
            parts=[genai_types.Part(text=input_query)]
        )

        events = self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_content,
        )

        response_parts = []
        async for event in events:
            if hasattr(event, "content") and event.content:
                for part in getattr(event.content, "parts", []):
                    if hasattr(part, "text") and part.text and not getattr(part, "thought", False):
                        response_parts.append(part.text)

        response_message = "".join(response_parts).strip()
        boxed_log(f"Response Message: {response_message}", logger, level="info")
        return response_message
        
