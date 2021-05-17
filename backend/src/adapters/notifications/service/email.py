from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from flask import current_app
from jinja2 import Environment, FileSystemLoader
import ssl
import smtplib


class EmailService:

    def __init__(self, host: str, port: str, user: str, password: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.env = Environment(loader=FileSystemLoader('%s/../templates/' % os.path.dirname(__file__)))

    @classmethod
    def from_config(cls, config):
        return cls(
            host=config.EMAIL_HOST,
            port=config.EMAIL_PORT,
            user=config.EMAIL_USER,
            password=config.EMAIL_PASSWORD
        )

    def send_email(self, to_email: str, subject: str, template_name: str = None, content: str = None, **kwargs):
        context = ssl.create_default_context()
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = self.user
        message['To'] = to_email
        if template_name:
            template = self.env.get_template('invite_evenement.html')
            body_content = template.render(**kwargs)
            message.attach(MIMEText(body_content, "html"))
        else:
            message.attach(MIMEText(content, 'plain'))

        msg_body = message.as_string()

        with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
            server.login(self.user, self.password)
            result = server.sendmail(self.user, to_email, msg_body)
            current_app.logger.info(f"result {result}")
