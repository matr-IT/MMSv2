from django.core.management.base import BaseCommand

from mail_management_service.services import send_mailing


class Command(BaseCommand):
    help = "Отправляет рассылку по заданному ID"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID рассылки для отправки")

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        try:
            result = send_mailing(mailing_id)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Рассылка {mailing_id} отправлена: {result['success_count']} успешно, {result['fail_count']} неудачно из {result['total']}."
                )
            )
        except ValueError as e:
            self.stdout.write(self.style.ERROR(str(e)))
