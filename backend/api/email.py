from djoser import utils
from djoser.conf import settings
from djoser.email import ActivationEmail, PasswordResetEmail
from templated_mail.mail import BaseEmailMessage

from users.tokens import custom_token_generator


class CustomActivationEmail(ActivationEmail):
    template_name = 'email/custom_activation.html'

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context['uid'] = utils.encode_uid(user.pk)
        context['token'] = custom_token_generator.make_token(user)
        context['url'] = settings.ACTIVATION_URL.format(**context)
        return context


class InvitationEmail(BaseEmailMessage):
    template_name = "email/invitation.html"

    def get_context_data(self):
        context = super().get_context_data()
        return context


class CustomPasswordResetEmail(PasswordResetEmail):
    template_name = "email/custom_password_reset.html"
