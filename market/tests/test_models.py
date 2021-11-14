from django.test import TestCase
from market.models import User, Group, Product, Category


class TestCourse(TestCase):
    def setUp(self):

        self.test_group = Group.objects.create(id="1", name="user")
        self.test_user = User.objects.create(
            username="Testing",
            email="test_email@gmail.com",
            password="test",
            groups=self.test_group,
            is_supplier=True,
        )

        self.test_category = Category.objects.create(id="1", name="Gadgets")
        self.test_product = Product.objects.create(
            title="Lenovo",
            description="Laptop",
            price=32000,
            supplier=self.test_user,
            product_category=self.test_category,
        )

    def test_username(self):
        result = User.objects.get(username=self.test_user)
        expected_object = f"{result.username}"
        self.assertEqual(str(result), expected_object)

    def test_product_title(self):
        result = Product.objects.get(title=self.test_product)
        expected_object = f"{result.title}"
        self.assertEqual(str(result), expected_object)

    def test_category_name(self):
        result = Category.objects.get(name=self.test_category)
        expected_object = f"{result.name}"
        self.assertEqual(str(result), expected_object)
