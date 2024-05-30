from django.urls import path
from chat.views import ChatRoomView  , MessagesView

urlpatterns = [
	path('room', ChatRoomView.as_view(), name='create chatRoom'),
	path('rooms/<int:userId>/', ChatRoomView.as_view(), name='get chatRoomList'),
    path('room/<str:roomId>/messages', MessagesView.as_view(), name='messageList'),
]