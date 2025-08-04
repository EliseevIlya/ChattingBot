from app.reposetory.message_repository import MessageRepository


class MessageService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository
