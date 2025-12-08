from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Product


class Command(BaseCommand):
    help = "Demonstration of bulk actions"

    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk actions")

        # возьмём любого существующего пользователя (или конкретного по username)
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR(
                "Нет ни одного пользователя. Создайте пользователя (createsuperuser) и запустите снова."
            ))
            return

        products = [
            Product(
                name=f"Smartphone {i}",
                description="",
                price=price,
                created_by=user,         # <-- ОБЯЗАТЕЛЬНО
            )
            for i, price in (
                (1, 199),
                (2, 299),
                (3, 399),
            )
        ]

        result = Product.objects.bulk_create(products)
        self.stdout.write(f"Created {len(result)} products")
        self.stdout.write("Done")
