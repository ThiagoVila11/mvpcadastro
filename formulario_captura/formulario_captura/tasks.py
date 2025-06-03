from celery import shared_task
from django.core.mail import send_mail

@shared_task
def enviar_email_agendado():
    send_mail(
        'Assunto Programado',
        'Este é o corpo do e-mail enviado automaticamente.',
        'thiagaotosatti@gmail.com',
        ['thiagaotosatti@gmail.com'],
        fail_silently=False,
    )
