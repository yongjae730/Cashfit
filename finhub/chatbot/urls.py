from django.urls import path
from .views import chatbot_response

urlpatterns = [
    path('get-response/', chatbot_response, name='chatbot_response'),
]
