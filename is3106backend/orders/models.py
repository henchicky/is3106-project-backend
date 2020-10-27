from django.db import models
from django.utils import timezone

from datetime import timedelta
import uuid
from recipes.models import Recipe


class Groupbuy(models.Model):
    gb_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    current_order_quantity = models.PositiveIntegerField(default=0)
    minimum_order_quantity = models.PositiveIntegerField(blank=True, null=True)
    approval_status = models.BooleanField(default=False)
    order_by = models.DateTimeField()
    final_price = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    fulfillment_date = models.DateTimeField(default=timezone.now()+timedelta(days=7))
    delivery_fee = models.DecimalField(decimal_places=2, max_digits=6, default=None, null=True)

    # Recipe ref, set null when recipe is deleted
    recipe = models.OneToOneField(Recipe, on_delete=models.SET_NULL, null=True)

    # vendor ref, set null when vendor is deleted
    vendor = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)

    groupbuys = models.Manager()

    # method to get groupbuy status
    def get_status(self):
        if timezone.now() > self.fulfillment_date: 
            return "DELIVERED" if self.approval_status and self.current_order_quantity >= self.minimum_order_quantity else "GROUPBUY_EXPIRED"
        # end if

        if not self.approval_status: return "PENDING_APPROVAL"
        if timezone.now() < self.order_by: return "GROUPBUY_IN_PROGRESS"

        return "DELIVERY_IN_PROGRESS"
    # end def

    def __str__(self):
        return f'Groupbuy ID: {self.gb_id}'
    # end def
# end class

class Order(models.Model):
    o_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    order_date = models.DateTimeField(default=timezone.now, editable=False)
    order_quantity = models.PositiveSmallIntegerField()
    order_price = models.DecimalField(decimal_places=2, max_digits=6)
    contact_number = models.CharField(max=15, null=True)

    # user who placed order, deleted when user is deleted
    buyer = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True)

    # delivery address of buyer, set null when delivery address is deleted
    delivery_address = models.ForeignKey('users.DeliveryAddress', on_delete=models.SET_NULL, null=True)

    # group buy ref, set null when group buy is deleted
    groupbuy = models.ForeignKey('Groupbuy', on_delete=models.SET_NULL, null=True)

    orders = models.Manager()

    def __str__(self):
        return f'Order ID: {self.o_id}'
    #end def
# end class
