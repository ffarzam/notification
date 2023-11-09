from typing import List
import yagmail

from config.config import get_settings

from utils.email_utils import template_mapper

settings = get_settings()


def send_email(user_mail: List[str], code: str, subject: str):
    # template = template_mapper(subject, code)
    #
    # message = MessageSchema(
    #     subject=subject,
    #     recipients=user_mail,
    #     body=template,
    #     subtype="html"
    # )
    #
    # fm = FastMail(conf)
    # await fm.send_message(message)

    port = settings.MAIL_PORT
    smtp_server = settings.MAIL_SERVER
    login = settings.MAIL_USERNAME
    password = settings.MAIL_PASSWORD

    sender_email = settings.MAIL_FROM
    receiver_email = user_mail

    template = template_mapper(subject, code)

    yag_smtp_connection = yagmail.SMTP(
        user=login,
        password=password,
        host=smtp_server)

    yag_smtp_connection.send(receiver_email, subject, template)
