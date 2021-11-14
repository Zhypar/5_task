from django.contrib import admin

from market.models import (
    User,
    Category,
    Product,
    Comments,
    CartItems,
    Orders,
    OrderItems,
)

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comments)
admin.site.register(CartItems)
admin.site.register(Orders)
admin.site.register(OrderItems)
