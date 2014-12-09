
errors = {
    'UserAlreadyExists': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'ResourceAlreadyExists': {
        'message': 'This resource already exists',
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID does not exist.",
        'status': 404,
    },
    'NotAuthorized': {
        'message': 'You are not authorized to perform this operation',
        'status': 401,
    },
    'PermissionDenied': {
        'message': 'This resource does not exist or you do not have '
                   'permissions to access this resource.',
        'status': 404,
    },
}
