from django.conf import settings
from django.core.mail import EmailMessage
import threading

from custom_logger import CustomLogger
from core.mail_messages import messages


custom_logger = CustomLogger()

def send_email(**kargs):
    request = kargs.get("request")
    recipient_list = kargs.get("recipient_list")

    if not recipient_list:
        if request:
            recipient_list = [request.user.email,]
        else:
            raise Exception("No recipients!")

    subject = kargs.get("subject") or 'welcome to shulehub'
    message = kargs.get("message") or 'Hi, thank you for choosing shulehub.'
    template_data = messages(kargs.get("template"), kargs)
    bcc_list = kargs.get("bcc_list")

    if template_data:
        subject = template_data["subject"]
        message = template_data["message"]

    try:
        email_from = settings.EMAIL_HOST_USER
        email = EmailMessage(subject, message, email_from, recipient_list, bcc_list,
            reply_to=[request.user.email, settings.EMAIL_HOST_USER,],
            headers={},
        )
        email.content_subtype = "html"
        thread = threading.Thread(target=email.send, args=[])
        thread.start()
    except Exception as e:
        print("ERROR: ",e)
        custom_logger.log_error("EMAIL", str(e), request, "send_email")
