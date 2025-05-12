from .config import app
from .services import MessageService

@app.get("/{message_id}")
async def home(message_id: int):
    """
    A simple home endpoint that returns a message by its ID.
    """
    return MessageService().get_message_by_id(message_id)