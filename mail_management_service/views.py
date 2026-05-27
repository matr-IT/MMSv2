from django.shortcuts import render

from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

from .models import Mailing, Recipient, Message, MailingAttempt

def send_mailing(request, mailing_id):
    from .services import send_mailing

    try:
        result = send_mailing(mailing_id)
        context = {
            "result": result,
            "mailing_id": mailing_id,
        }
        return render(request, "send_result.html", context)
    except ValueError as e:
        context = {
            "error": str(e),
            "mailing_id": mailing_id,
        }
        return render(request, "send_error.html", context)

def index(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status="in_progress").count()
    total_recipients = Recipient.objects.count()

    context = {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "total_recipients": total_recipients,
    }

    return render(request, "index.html", context)

def user_stats(request):
    mailings_count = Mailing.objects.count()
    recipients_count = Recipient.objects.count()
    messages_count = Message.objects.count()
    attempts_count = MailingAttempt.objects.count()

    context = {
        "mailings_count": mailings_count,
        "recipients_count": recipients_count,
        "messages_count": messages_count,
        "attempts_count": attempts_count,
    }
    return render(request, "user_stats.html", context)

class RecipientListView(ListView):
    model = Recipient
    template_name = "recipient_list.html"
    context_object_name = "recipients"


class RecipientCreateView(CreateView):
    model = Recipient
    fields = ["email", "name", "comment"]
    template_name = "recipient_form.html"
    context_object_name = "recipients"
    success_url = reverse_lazy("mail_management_service:recipient-list")


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = "recipient_detail.html"
    context_object_name = "recipient"


class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ["email", "name", "comment"]
    template_name = "recipient_form.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("mail_management_service:recipient-list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "recipient_confirm_delete.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("mail_management_service:recipient-list")


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing_list.html"
    context_object_name = "mailings"


class MailingCreateView(CreateView):
    model = Mailing
    fields = ["start_time", "end_time", "message", "recipients", "status"]
    template_name = "mailing_form.html"
    context_object_name = "mailings"
    success_url = reverse_lazy('mail_management_service:mailing-list')


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailing_detail.html"
    context_object_name = "mailing"


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ["start_time", "end_time", "message", "recipients"]
    template_name = "mailing_form.html"
    context_object_name = "mailing"
    success_url = reverse_lazy('mail_management_service:mailing-list')



class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing_confirm_delete.html"
    context_object_name = "mailing"
    success_url = reverse_lazy('mail_management_service:mailing-list')



class MessageListView(ListView):
    model = Message
    template_name = "message_list.html"
    context_object_name = "messages"


class MessageCreateView(CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "message_form.html"
    context_object_name = "messages"
    success_url = reverse_lazy("mail_management_service:message-list")


class MessageDetailView(DetailView):
    model = Message
    template_name = "message_detail.html"
    context_object_name = "message"


class MessageUpdateView(UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "message_form.html"
    context_object_name = "message"
    success_url = reverse_lazy("mail_management_service:message-list")



class MessageDeleteView(DeleteView):
    model = Message
    template_name = "message_confirm_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("mail_management_service:message-list")



class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "mailing_attempt_list.html"
    context_object_name = "attempts"


class MailingAttemptDetailView(DetailView):
    model = MailingAttempt
    template_name = "mailing_attempt_detail.html"
    context_object_name = "attempt"

