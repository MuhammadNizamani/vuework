class UserDoesNotExist(Exception):
    def __init__(self, message="User does not exist"):
        self.message = message
        super().__init__(self.message)