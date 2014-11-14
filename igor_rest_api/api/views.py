from flask.ext.restful import Resource

# Root endpoint, used to test connection
"""
    GET     /                 Returns 200 OK with a message
"""
class RootAPI(Resource):
    def get(self):
        return {'message': 'Igor lives!'}