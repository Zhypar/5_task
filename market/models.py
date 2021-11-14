from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from market.managers import UserAccountManager
from market.statuses import STATUS_NONE, PURCHASED, ONE, TWO, THREE, FOUR, FIVE, ZERO
from django.utils.translation import gettext_lazy as _


class User(AbstractUser, models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=False, blank=True, null=True)
    is_supplier = models.BooleanField(_("supplier"), default=False)
    groups = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="market_groups",
    )
    password = models.CharField(max_length=100, blank=True, null=True)

    objects = UserAccountManager()

    REQUIRED_FIELDS = ["groups_id", "email"]
    USERNAME_FIELD = "username"
    REQUIRED_ADMIN_FIELDS = ["email"]

    def __str__(self):
        return self.username.__str__()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class Product(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=500, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    supplier = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        limit_choices_to={"is_supplier": True},
        null=True,
        blank=True,
    )
    product_category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, related_name="category"
    )

    def __str__(self):
        return self.title.__str__()

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name.__str__()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Comments(models.Model):
    RATE_CHOICES = (
        (ZERO, _("0")),
        (ONE, _("1")),
        (TWO, _("2")),
        (THREE, _("3")),
        (FOUR, _("4")),
        (FIVE, _("5")),
    )

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rate = models.CharField(
        choices=RATE_CHOICES, max_length=100, blank=True, null=True, default=ZERO
    )
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=300, blank=True, default="text")
    replies = models.ForeignKey(
        "Comments", on_delete=models.CASCADE, null=True, related_name="add_replies"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, related_name="product"
    )

    def repliess(self):
        return self.add_replies.all().values("id", "user_id", "text", "date")

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class CartItems(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, related_name="product_id"
    )
    customer_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    amount = models.IntegerField(blank=False, default=0)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class Orders(models.Model):

    PRODUCT_STATUS = (
        (STATUS_NONE, _("None")),
        (PURCHASED, _("Purchased")),
    )

    id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=PRODUCT_STATUS,
        max_length=100,
        blank=True,
        null=True,
        default=STATUS_NONE,
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItems(models.Model):
    id = models.AutoField(primary_key=True)
    orders = models.ForeignKey(
        Orders, on_delete=models.CASCADE, null=True, blank=True, related_name="orders"
    )
    prod_id = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prod_id",
    )
    title = models.CharField(max_length=100, blank=True, default="product_title")
    description = models.CharField(
        max_length=500, blank=True, default="product_description"
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.IntegerField(blank=False, default=0)

    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"
