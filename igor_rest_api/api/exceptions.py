
class ResourceAlreadyExists(Exception):
    def __init__(self, message="Resource already exists"):
        self.message = message

    def __str__(self):
        return self.message

class UserAlreadyExists(ResourceAlreadyExists):
    def __init__(self, user,
            message="A user with the username '{user}'' already exists!"):
        self.user = user
        self.message = message

    def __str__(self):
        return self.message.format(user=self.user)

class ResourceDoesNotExist(Exception):
    def __init__(self, message="Resource does not exist"):
        self.message = message

    def __str__(self):
        return self.message

class NotAuthorized(Exception):
    def __init__(self, user):
        self.user = user

    def __str__(self):
        return "User %s is not authorized to perform this operation" % self.user

class PermissionDenied(Exception):
    pass
