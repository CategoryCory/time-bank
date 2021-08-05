from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
import json

from .models import UserMessageThread, UserMessage
from .serializers import MessageSerializer, MessageThreadSerializer

CustomUser = get_user_model()


@login_required
def get_message_threads_by_user(request):
    if request.user.is_authenticated:
        u = request.user
        return_dict = {}
        job_id = request.GET.get('job-id')
        sender_id = request.GET.get('sender')
        if job_id is not None:
            message_threads = UserMessageThread.objects.filter(job=job_id)
            if sender_id is not None:
                message_threads = message_threads.filter(created_by=sender_id)
        else:
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
        sender_id = data['sender']
        recipient_id = data['recipient']
        message = data['message']
        thread_id = data['thread']

        msg = UserMessage(sender_id=sender_id, recipient_id=recipient_id, message_body=message, thread_id=thread_id)
        msg.save()

        # Send email
        recipient = CustomUser.objects.get(id=recipient_id)
        email_subject = 'Sullivan Foundation Time Bank Response'
        email_body = (
            f'You have a new message on the Sullivan Time Bank.\n'
            f'To view this message, please log into your account at https://sullivantimebank.org/accounts/login/ \n'
            f'Please do not reply to this email.\n'
        )
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [recipient.email],
            fail_silently=True
        )

        return JsonResponse({'new_msg_id': msg.id}, status=201)
    else:
        return JsonResponse({'message': 'Method not allowed.'}, status=405)
    