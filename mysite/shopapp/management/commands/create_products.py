from django.core.management import BaseCommand

from shopapp.models import Product

class Command(BaseCommand):
    """"
    Create products
    """
    def handle(self, *args, **options):
        self.stdout.write("Create products")
        products_names = [
            "Laptop",
            "Desktop",
            "Smartphone",
        ]
        for products_names in products_names:
            product, created = Product.objects.get_or_create(name=products_names)
            self.stdout.write(f"Created product {product.name}")

        self.stdout.write(self.style.SUCCESS("Product created"))