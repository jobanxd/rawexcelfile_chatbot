import logging
from fastapi import APIRouter, HTTPException
from models.chatbot_agent import (
    ChatbotAgentRequest,
    ChatbotAgentResponse,
)
from services.chatbot_agent import ChatbotService

router = APIRouter()
logger = logging.getLogger(__name__)
chatbot_service = ChatbotService()


@router.post("/generate", response_model=ChatbotAgentResponse)
async def generate_respones(request: ChatbotAgentRequest):
    try:
        response_message = await chatbot_service.generate_response(
            user_id=request.user_id,
            session_id=request.session_id,
            input_query=request.input_query,
        )

        return ChatbotAgentResponse(
            response=response_message,
        )
    
    except Exception as e:
        logger.exception("Error generating chatbot response")
        raise HTTPException(status_code=500, detail=str(e))
    