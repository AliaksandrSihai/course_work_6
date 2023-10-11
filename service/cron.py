import datetime
from django.core.mail import send_mail
from config import settings
from service.models import NewsletterSettings, NewsletterMessage, LogsNewsletter


class SomeError(Exception):
    """Класс для создания пользовательского исключения"""
    def __init__(self):
        self.message = 'Возникла какая-то ошибка'


def send_message(subject: str, message: str, recipient_list: list):
    """Функция отправки сообщения"""
    send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list
        )
    return True


def new_log(attempt_status, answer, pk):
    """Функция создания лога"""
    LogsNewsletter.objects.create(attempt_status=attempt_status,
                                  server_response=answer,
                                  newsletter_id=pk)


def send_newsletter():
    """Реализация отправки рассылки"""
    now = datetime.date.today()
    all_newsletters = NewsletterSettings.objects.all()
    for newsletter in all_newsletters:
        if newsletter.newsletter_start <= now <= newsletter.newsletter_finish:
            newsletter.status = 'Запущена'
            newsletter.save()
            info = newsletter.newslettermessage_set.all()
            for data in info:
                to_email = [client.contact_email for client in data.to_email.all()]
                newsletter_body = data.newsletter_body
                newsletter_name = data.newsletter_name
                send_letter = send_message(
                    subject=f'Рассылка {newsletter_name}',
                    message=f'{newsletter_body}',
                    recipient_list=to_email,
                )
                if send_letter:
                    new_log(attempt_status=True,
                            answer=f'Рассылка {newsletter_name} отправлена: {to_email}',
                            pk=data)
                else:
                    new_log(attempt_status=False,
                            answer=f'Рассылка {newsletter_name} не отправлена: {to_email}',
                            pk=data)
                    raise SomeError
        elif now < newsletter.newsletter_start:
            newsletter.status = 'Будет запущена'
            newsletter.save()
            pass
        else:
            newsletter.status = 'Завершена'
            newsletter.save()


def newsletter():
    """Функция запуска проверки частоты отправки и обработки исключений рассылки"""
    try:
        today = datetime.date.today()
        all_messages = NewsletterMessage.objects.all()
        for message in all_messages:
            frequency = message.newsletter_settings.frequency
            if frequency == 'Раз в день':
                send_newsletter()
            elif frequency == 'Раз в неделю' and today.weekday() == 0:
                send_newsletter()
            elif frequency == 'Раз в месяц' and today.day == 1:
                send_newsletter()
    except SomeError as e:
        print(e.message)
