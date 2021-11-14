from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from django.contrib.auth.models import Group
from market.models import (
    User,
    Product,
    Category,
    Comments,
    CartItems,
    Orders,
    OrderItems,
)
from market import service


class AllGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            "id",
            "name",
        ]


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "groups",
            "is_supplier",
        ]


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "groups",
            "is_supplier",
        ]
        read_only_fields = [
            "id",
            "is_supplier",
        ]

    def validate(self, args):
        email = args.get("email", None)
        username = args.get("username", None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ("email already exists")})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": ("username already exists")})

        return super().validate(args)


class CreateSuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "groups",
        ]

    def create(self, validated_data):
        superuser = User.objects._create_superuser(
            username=validated_data.__getitem__("username"),
            groups=validated_data.__getitem__("groups"),
            email=validated_data.__getitem__("email"),
            password=validated_data.__getitem__("password"),
        )

        return superuser


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "is_supplier",
        ]


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class UpdateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class GetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
        ]


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "creation_date",
            "price",
            "supplier",
            "product_category",
        ]


class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "creation_date",
            "price",
            "supplier",
            "product_category",
        ]


class GetProductSerializer(serializers.ModelSerializer):

    product_category = GetCategorySerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "creation_date",
            "price",
            "supplier",
            "product_category",
        ]


class CreateOrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = [
            "id",
            "prod_id",
            "title",
            "description",
            "creation_date",
            "price",
            "amount",
        ]
        read_only_fields = ["id" "creation_date"]


class UpdateOrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = [
            "id",
            "prod_id",
            "title",
            "description",
            "creation_date",
            "price",
            "amount",
        ]
        read_only_fields = ["id" "creation_date"]


class GetOrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = [
            "id",
            "prod_id",
            "title",
            "description",
            "creation_date",
            "price",
            "amount",
        ]


class CreateOrderSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):

    order_items = CreateOrderItemsSerializer(
        many=True, allow_null=True, source="orders"
    )
    status = service.ChoiceField(choices=Orders.PRODUCT_STATUS)

    class Meta:
        model = Orders
        fields = [
            "id",
            "client_id",
            "order_items",
            "address",
            "phone",
            "date",
            "status",
        ]
        read_only_fields = [
            "id",
            "client_id",
            "order_items",
            "date",
            "status",
        ]


class UpdateOrderSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):

    order_items = UpdateOrderItemsSerializer(
        many=True, allow_null=True, source="orders"
    )
    status = service.ChoiceField(choices=Orders.PRODUCT_STATUS)

    class Meta:
        model = Orders
        fields = [
            "id",
            "client_id",
            "order_items",
            "address",
            "phone",
            "date",
            "status",
        ]
        read_only_fields = [
            "id",
            "client_id",
            "order_items",
            "date",
            "status",
        ]


class GetOrderSerializer(serializers.ModelSerializer):

    order_items = GetOrderItemsSerializer(many=True, source="orders")
    status = service.ChoiceField(choices=Orders.PRODUCT_STATUS)

    class Meta:
        model = Orders
        fields = [
            "id",
            "client_id",
            "order_items",
            "address",
            "phone",
            "date",
            "status",
        ]


class CreateCartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = "__all__"
        read_only_fields = [
            "id",
            "customer_id",
        ]


class UpdateCartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = "__all__"
        read_only_fields = [
            "id",
            "customer_id",
        ]


class GetCartItemsSerializer(serializers.ModelSerializer):

    product_id = GetProductSerializer()

    class Meta:
        model = CartItems
        fields = [
            "id",
            "product_id",
            "amount",
        ]


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        exclude = [
            "replies",
        ]
        read_only_fields = [
            "id",
            "user_id",
            "date",
        ]


class CreateRelpliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            "replies",
            "text",
        ]
        read_only_fields = [
            "id",
            "user_id",
            "date",
        ]


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"
        read_only_fields = [
            "id",
            "user_id",
        ]


class GetCommentSerializer(serializers.ModelSerializer):

    user_id = serializers.StringRelatedField()

    class Meta:
        model = Comments
        fields = [
            "id",
            "user_id",
            "rate",
            "date",
            "text",
            "product",
            "replies",
        ]


class NotSerializer(serializers.Serializer, object):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
