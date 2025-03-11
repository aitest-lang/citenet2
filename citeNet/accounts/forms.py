# accounts/forms.py
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string

class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email_list, html_email_template_name=None):
        """
        Send a password reset email to the user.
        """
        subject = "Password Reset Request" # Hardcoded subject
        message_html = render_to_string(email_template_name, context) # HTML version
        recipient_list = [to_email_list] # Ensure recipient_list is a list

        send_mail(
            subject,
            "", # Empty plain-text message
            from_email,
            recipient_list,
            html_message=message_html, # Provide HTML content here
        )
