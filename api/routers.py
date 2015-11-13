from swampdragon import route_handler
from swampdragon.route_handler import ModelPublisherRouter
from .serializers import ChatSerializer
from .models import Chat


class ChatRouter(ModelPublisherRouter):
    serializer_class = ChatSerializer
    model = Chat
    route_name = 'chat'

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['pk'])

    def get_query_set(self, **kwargs):
        return self.model.all()

route_handler.register(ChatRouter)
