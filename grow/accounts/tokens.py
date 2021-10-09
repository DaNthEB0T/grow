from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class VerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_validated)
        )

class PasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.password)
        )

verification_token_generator = VerificationTokenGenerator()

password_reset_token_generator = PasswordResetTokenGenerator()

