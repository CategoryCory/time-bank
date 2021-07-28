from django.urls import path

from .views import get_message_threads_by_user, get_messages_by_thread, submit_new_message

app_name = 'user_messages'
urlpatterns = [
    path('threads/', get_message_threads_by_user, name='message_threads'),
    path('threads/<int:thread_id>/', get_messages_by_thread, name='message_list_by_thread'),
    path('threads/submit-new-message/', submit_new_message, name='submit_new_message'),
]