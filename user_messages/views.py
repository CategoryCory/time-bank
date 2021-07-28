from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
import json

from .models import UserMessageThread, UserMessage
from .serializers import MessageSerializer, MessageThreadSerializer


@login_required
def get_message_threads_by_user(request):
    if request.user.is_authenticated:
        u = request.user
        return_dict = {}
        message_threads = UserMessageThread.objects.filter(Q(created_by=u)|Q(recipient=u))
        serializer = MessageThreadSerializer(message_threads, many=True, context={'request': request})
        return_dict['current_user_id'] = u.id
        return_dict['current_user'] = u.email
        return_dict['message_threads'] = serializer.data
        return JsonResponse(return_dict, safe=False)
    else:
        return JsonResponse({'message': 'Access denied.'}, status=401)


@login_required
def get_messages_by_thread(request, thread_id):
    if request.user.is_authenticated:
        messages = UserMessage.objects.filter(thread=thread_id).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'message': 'Access denied.'}, status=401)


@login_required
def submit_new_message(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        sender = data['sender']
        recipient = data['recipient']
        message = data['message']
        thread = data['thread']

        msg = UserMessage(sender_id=sender, recipient_id=recipient, message_body=message, thread_id=thread)
        msg.save()
        return JsonResponse({'new_msg_id': msg.id}, status=201)
    else:
        return JsonResponse({'message': 'Method not allowed.'}, status=405)
    