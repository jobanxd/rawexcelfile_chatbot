from pydantic import BaseModel

class ChatbotAgentRequest(BaseModel):
    session_id: str
    user_id: str
    input_query: str

class ChatbotAgentResponse(BaseModel):
    response: str