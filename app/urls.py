from app.handlers.hello import Hello
from app.handlers.token import NewToken, AssignToken
from app import api



api.add_resource(Hello, '/hello')
api.add_resource(NewToken, '/new-token')
api.add_resource(AssignToken, '/assign-token')


