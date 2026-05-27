from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Recipient(models.Model):
    email = models.EmailField(verbose_name="электронная почта")
    name = models.CharField(max_length=100, verbose_name="имя", blank=True, null=True)
    comment = models.TextField(verbose_name="комментарий", blank=True, null=True)


    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "получатель"
        verbose_name_plural = "получатели"
        ordering = ["email"]


class Message(models.Model):
    subject = models.CharField(max_length=200, verbose_name="тема")
    body = models.TextField(verbose_name="тело сообщения")

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"


class Mailing(models.Model):
    start_time = models.DateTimeField(verbose_name="время начала")
    end_time = models.DateTimeField(verbose_name="время окончания")
    status = models.CharField(
        max_length=50,
        verbose_name="статус",
        choices=[
            ("created", "Создана"),
            ("in_progress", "Запущена"),
            ("completed", "Завершена"),
        ],
    )
    disabled = models.BooleanField(default=False, verbose_name="Отключена")

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="сообщение",
    )
    recipients = models.ManyToManyField(
        Recipient, related_name="mailings", verbose_name="получатели"
    )

    def clean(self):
        now = timezone.now()
        if self.start_time and self.end_time:
            if self.start_time < now:
                raise ValidationError(
                    {"start_time": "Время начала не может быть в прошлом."}
                )
            if self.start_time >= self.end_time:
                raise ValidationError(
                    {"end_time": "Время окончания должно быть позже времени начала."}
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Рассылка с {self.start_time} по {self.end_time} - Статус: {self.status}"
        )

    def update_status(self):

        now = timezone.now()
        if self.disabled:
            self.status = "created"
        elif self.start_time <= now < self.end_time:
            self.status = "in_progress"
        elif now >= self.end_time:
            self.status = "completed"
        else:
            self.status = "created"
        self.save()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ["-start_time"]


class MailingAttempt(models.Model):
    attempt_time = models.DateTimeField(verbose_name="дата отправки", auto_now=True)
    status = models.CharField(
        max_length=50,
        verbose_name="статус",
        choices=[("success", "Успешно"), ("failed", "Неудачно")],
    )
    server_response = models.TextField(
        verbose_name="ответ сервера", blank=True, null=True
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="рассылка",
    )

    class Meta:
        verbose_name = "попытка отправки"
        verbose_name_plural = "попытки отправки"
        ordering = ["-attempt_time"]
