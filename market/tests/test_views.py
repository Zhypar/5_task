from rest_framework.test import APITestCase
from market.models import User, Group, Product, Category, Comments, CartItems, Orders
from rest_framework import status


class TestUser(APITestCase):
    url_users = "/api/user/find_all_users/"
    url_a_user = "/api/user/find_user_by_id/?id=1/"
    url_access_token = "/api/user/access_token/"
    url_refresh_token = "/api/user/refresh_token/"
    url_registration = "/api/user/registration/?"
    url_delete_user = "/api/user/delete_user_by_id/?id=1/"
    url_delete_all_users = "/api/user/delete_all_users"
    url_update_user = "/api/user/update_user_by_id/?id=1/"

    def setUp(self):

        global test_group
        test_group = Group.objects.create(id="1", name="user")
        test_user = User.objects.create(
            username="Testing",
            email="test_email@gmail.com",
            password="test",
            groups=test_group,
        )

    def test_get_users(self):
        response = self.client.get(self.url_users)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["username"], "Testing")

    def test_create_user(self):

        data = {
            "username": "Testuser",
            "email": "testuser@gmail.com",
            "password": "test",
            "groups": 1,
        }
        response = self.client.post(self.url_registration, data=data, format="json")
        result = response.json()
        self.assertEqual(response.status_code, 201)

    def test_create_with_existing_email(self):

        data = {
            "username": "Testing",
            "email": "testuser@gmail.com",
            "password": "test",
            "groups": 1,
        }
        response = self.client.post(self.url_registration, data=data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_with_existing_username(self):

        data = {
            "username": "Testing",
            "email": "test@gmail.com",
            "password": "test",
            "groups": 1,
        }
        response = self.client.post(self.url_registration, data=data, format="json")
        self.assertEqual(response.status_code, 400)


class AuthViewsTests(APITestCase):

    url_users = "/api/user/find_all_users/"
    url_find_user = "/api/user/find_user_by_id/"
    url_refresh_token = "/api/user/refresh_token/"
    url_registration = "/api/user/registration/?"
    url_update_user = "/api/user/update_user_by_id/"
    url_delete_user = "/api/user/delete_user_by_id/"
    url_all_products = "/api/product/find_all_products/"
    url_find_product = "/api/product/find_product_by_id/"
    url_create_product = "/api/product/create_product/"
    url_delete_product = "/api/product/delete_product_by_id/"
    url_update_product = "/api/product/update_product_by_id/"
    url_all_categories = "/api/category/find_all_categories/"
    url_find_category = "/api/category/find_category_by_id/"
    url_create_category = "/api/category/create_category/"
    url_delete_category = "/api/category/delete_category_by_id/"
    url_update_category = "/api/category/update_category_by_id/"
    url_all_comments = "/api/comments/find_all_comments/"
    url_find_comment = "/api/comments/find_comment_by_id/"
    url_create_comment = "/api/comments/create_comment/"
    url_delete_comment = "/api/comments/delete_comment_by_id/"
    url_update_comment = "/api/comments/update_comment_by_id/"
    url_create_replies = "/api/comments/create_replies/"
    url_all_groups = "/api/group/find_all_groups/"
    url_all_cartitems = "/api/cartitem/find_all_cartitems/"
    url_create_cartitem = "/api/cartitem/create_cartitem/"
    url_update_cartitem = "/api/cartitem/update_cartitem_by_id/"
    url_find_cartitem = "/api/cartitem/find_cartitem_by_id/"
    url_delete_cartitem = "/api/cartitem/delete_cartitem_by_id/"
    url_create_order = "/api/order/create_order/"
    url_all_orders = "/api/order/find_all_orders/"

    def setUp(self):
        global test_group
        test_group = Group.objects.create(id="1", name="user")
        global test_user
        test_user = User.objects.create_user(
            username="Testing",
            email="test_email@gmail.com",
            password="test",
            groups_id=1,
        )

        self.test_category = Category.objects.create(name="Gadgets")
        self.test_product = Product.objects.create(
            title="Lenovo",
            description="Laptop",
            price=32000,
            product_category=self.test_category,
        )

        self.test_comments = Comments.objects.create(
            text="Cool", product_id=self.test_product.pk
        )

        self.test_cartitem = CartItems.objects.create(
            product_id=self.test_product, customer_id=test_user, amount=1
        )

        self.test_order = Orders.objects.create(
            client_id=test_user, address="Bishkek", phone="0987654", total_price=1000
        )

    def test_everything(self):

        # URL using path name
        url = "/api/user/access_token/"

        # Create a user is a workaround in order to authentication works
        response = self.client.post(
            url, {"username": "Testing", "password": "test"}, format="json"
        )
        result = response.json()
        self.assertEqual(test_user.is_active, 1, "Active User")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        global token
        token = response.data["access_token"]

        self.client.credentials(HTTP_AUTHORIZATION="JWT {0}".format(token))
        data = {
            "title": "Testproduct",
            "description": "test_description",
            "price": 1000,
            "product_category": 1,
        }

        response = self.client.post(self.url_create_product, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "client_id": test_user.pk,
            "address": "Osh",
            "phone": "234567",
            "total_price": 1133,
        }

        response = self.client.post(self.url_create_order, data=data, format="json")
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "name": "House",
        }

        response = self.client.post(self.url_create_category, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {"text": "nice", "product_id": 1}
        response = self.client.post(self.url_create_comment, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "product_id": self.test_product.pk,
            "customer_id": test_user.pk,
            "amount": 2,
        }
        response = self.client.post(self.url_create_cartitem, data=data, format="json")
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.url_all_groups)
        result = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            result, {"detail": "You do not have permission to perform this action."}
        )

        response = self.client.get(self.url_all_cartitems)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["id"], self.test_cartitem.pk)

        response = self.client.get(self.url_all_orders)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["id"], self.test_order.pk)

        response = self.client.get(self.url_all_comments)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["id"], self.test_comments.pk)

        response = self.client.get(self.url_all_products)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["title"], "Lenovo")

        response = self.client.get(self.url_all_categories)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["id"], self.test_category.pk)

        response = self.client.patch(
            "{}{}/".format(self.url_update_product, self.test_product.pk),
            {
                "title": "Lenova",
                "description": "A new laptop",
                "price": 2000,
                "product_category": 1,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            "{}{}/".format(self.url_update_comment, 3),
            {"test": "nice and cool", "product_id": 1},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.patch(
            "{}{}/".format(self.url_update_category, self.test_category.pk),
            {
                "id": "1",
                "name": "New Gadgets",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            "{}{}/".format(self.url_update_cartitem, self.test_cartitem.pk),
            {
                "product_id": self.test_product.pk,
                "customer_id": test_user.pk,
                "amount": 4,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            "{}{}/".format(self.url_find_product, self.test_product.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            "{}{}/".format(self.url_find_category, self.test_category.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            "{}{}/".format(self.url_find_comment, self.test_comments.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            "{}{}/".format(self.url_update_user, test_user.pk),
            {"username": "Testing", "password": "newtest"},
            format="json",
        )
        result = response.json()
        print(result)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.url_refresh_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get("{}{}/".format(self.url_find_user, test_user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get("{}{}/".format(self.url_find_user, 2))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(
            "{}{}/".format(self.url_find_cartitem, self.test_cartitem.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(
            "{}{}/".format(self.url_delete_cartitem, self.test_cartitem.pk)
        )
        print(response.json)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(
            "{}{}/".format(self.url_delete_product, self.test_product.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(
            "{}{}/".format(self.url_delete_category, self.test_category.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete("{}{}/".format(self.url_delete_category, 3))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(
            "{}{}/".format(self.url_delete_user, test_user.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(
            "{}{}/".format(self.url_delete_user, test_user.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
