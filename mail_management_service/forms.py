from django import forms

from mail_management_service.models import Recipient, Message, Mailing


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "name", "comment"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "message", "recipients", "status"]
