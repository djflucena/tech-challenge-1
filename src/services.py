from .repositories import MessageRepository

class MessageService:
    """
    A simple service class to manage messages.
    """
    def __init__(self):
        self.messages_repository = MessageRepository()
    
    def get_message_by_id(self, message_id: int) -> str:
        """
        Returns a message by its ID.
        :param message_id: The ID of the message to retrieve.
        :return: The message associated with the given ID.
        :rtype: str
        """ 
        return self.messages_repository.get_message_by_id(message_id)