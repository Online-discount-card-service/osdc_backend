from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailActivateTokenGenerator(PasswordResetTokenGenerator):
    """Токен для активации почты, не портится после успешного логина."""

    def _make_hash_value(self, user, timestamp):
        email_field = user.get_email_field_name()
        email = getattr(user, email_field, "") or ""
        return f"{user.pk}{user.password}{timestamp}{email}"


custom_token_generator = EmailActivateTokenGenerator()
