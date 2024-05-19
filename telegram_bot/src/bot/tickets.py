class Ticket:
    def __init__(self, user_id, chat_id):
        self.user_id = user_id
        self.chat_id = chat_id
        self.flag = False
        self.name = None
        self.email = None
        self.diagnosis = None
        self.doctor = None
        self.status = None
        self.request = None
