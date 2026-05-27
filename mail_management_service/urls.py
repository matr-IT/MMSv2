from django.urls import path

import mail_management_service
from mail_management_service import views
from mail_management_service.apps import MailManagementServiceConfig
from mail_management_service.views import (
    MailingListView,
    MailingCreateView,
    MailingDetailView,
    MailingUpdateView,
    MailingDeleteView,
    RecipientListView,
    RecipientCreateView,
    RecipientDetailView,
    RecipientUpdateView,
    RecipientDeleteView,
    MessageListView,
    MessageDetailView,
    MessageUpdateView,
    MessageDeleteView,
    MessageCreateView, MailingAttemptListView, MailingAttemptDetailView,
)

app_name = MailManagementServiceConfig.name

urlpatterns = [
    path('', views.index, name='index'),
    path("user-stats/", views.user_stats, name="user-stats"),
    path('mailing-attempts/', MailingAttemptListView.as_view(), name='mailing-attempt-list'),
    path('mailing-attempts/<int:pk>/', MailingAttemptDetailView.as_view(), name='mailing-attempt-detail'),

    path("mailings/", MailingListView.as_view(), name="mailing-list"),
    path("mailings/create/", MailingCreateView.as_view(), name="mailing-create"),
    path("mailings/<int:pk>/", MailingDetailView.as_view(), name="mailing-detail"),
    path("mailings/<int:pk>/edit/", MailingUpdateView.as_view(), name="mailing-update"),
    path(
        "mailings/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing-delete"
    ),
    path("recipients/", RecipientListView.as_view(), name="recipient-list"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipient-create"),
    path(
        "recipients/<int:pk>/", RecipientDetailView.as_view(), name="recipient-detail"
    ),
    path(
        "recipients/<int:pk>/edit/",
        RecipientUpdateView.as_view(),
        name="recipient-update",
    ),
    path(
        "recipients/<int:pk>/delete/",
        RecipientDeleteView.as_view(),
        name="recipient-delete",
    ),
    path("messages/", MessageListView.as_view(), name="message-list"),
    path("messages/create/", MessageCreateView.as_view(), name="message-create"),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="message-detail"),
    path("messages/<int:pk>/edit/", MessageUpdateView.as_view(), name="message-update"),
    path(
        "messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message-delete"
    ),
    path('mailings/<int:mailing_id>/', views.send_mailing, name='send-mailing'),

]
