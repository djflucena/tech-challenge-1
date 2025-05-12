class MessageRepository:
    """
    A repository class to handle message-related operations.
    """

    def __init__(self):
        pass
    
    def get_message_by_id(self, message_id: int):
        """
        Simulate a database call to get a message by its ID.
        """
        messages = {
            1: "Hello, World!",
            2: "Goodbye, World!",
            3: "Hello, Universe!"
        }
        return messages.get(message_id, "Message not found")