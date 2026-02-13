from pydantic import BaseModel

class SendMessageRequest(BaseModel):
    sender_id: str
    receiver_id: str
    message: str


class ReceiveMessageRequest(BaseModel):
    user_id: str
    message_id: str
