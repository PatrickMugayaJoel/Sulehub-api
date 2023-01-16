from django.conf import settings
from django.core.mail import send_mail

from custom_logger import CustomLogger
from core.mail_messages import messages


custom_logger = CustomLogger()

def send_email(**args):
    request = args.get("request")
    recipient_list = args.get("recipient_list")

    if not recipient_list:
        if request:
            recipient_list = [request.user.email,]
        else:
            return

    subject = args.get("subject") or 'welcome to shulehub'
    message = args.get("message") or 'Hi, thank you for choosing shulehub.'
    template_data = messages(args.get("template"))

    if template_data:
        subject = template_data["subject"]
        message = template_data["message"]

    try:
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        print("ERROR: ",e)
        custom_logger.log_error("EMAIL", str(e), request, "send_email")
