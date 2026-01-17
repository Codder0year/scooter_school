from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from .models import News
from .serializers import NewsSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-date_posted')
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnly]


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def contact_view(request):
    """
    Ожидает JSON:
    {
      "name": "...",
      "message": "...",
      "phone": "..."
    }
    Попытается отправить email на EMAIL_HOST_USER (если настроено),
    иначе вернёт 200 и залогирует.
    """
    data = request.data
    name = data.get('name')
    message = data.get('message')
    phone = data.get('phone')

    if not name or not message:
        return Response({'detail': 'name и message обязательны'}, status=status.HTTP_400_BAD_REQUEST)

    subject = f"Сообщение с сайта от {name}"
    body_lines = [
        f"Имя: {name}",
        f"Телефон: {phone or 'Не указан'}",
        "",
        "Сообщение:",
        message
    ]
    body = "\n".join(body_lines)

    # Попытка отправить письмо, если настроена почта
    email_sent = False
    try:
        email_from = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', None)
        email_to = [getattr(settings, 'CONTACT_EMAIL', None) or email_from]
        if email_from and email_to and email_to[0]:
            send_mail(subject, body, email_from, email_to, fail_silently=False)
            email_sent = True
    except BadHeaderError:
        return Response({'detail': 'Invalid header found.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        # если почта не настроена или ошибка — просто логируем и возвращаем успех
        print(f"contact_view: mail send error: {e}")

    return Response({'ok': True, 'email_sent': email_sent}, status=status.HTTP_200_OK)
