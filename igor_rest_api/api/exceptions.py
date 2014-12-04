
class UserAlreadyExists(Exception):
    def __init__(self, user):
        self.user = user

    def __str__(self):
        return "A user with the username %s already exists!" % self.user

class ResourceDoesNotExist(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class NotAuthorized(Exception):
    def __init__(self, user):
        self.user = user

    def __str__(self):
        return "User %s is not authorized to perform this operation" % self.user
