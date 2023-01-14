from django.conf import settings
from django.core.mail import send_mail

from custom_logger import CustomLogger


custom_logger = CustomLogger()

def send_email(**args):
    if not args.get("recipient_list"):
        return
    
    email_from = settings.EMAIL_HOST_USER
    template = args.get("template")
    subject = args.get("subject") or 'welcome to GFG world'
    message = args.get("message") or 'Hi, thank you for choosing shulehub.'

    try:
        send_mail( subject, message, email_from, args.get("recipient_list"))
    except Exception as e:
        print("ERROR: ",e)
        custom_logger.log_error("EMAIL", str(e), args.get("request"), "send_email")
