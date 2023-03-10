from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_delete

from clients.models import Client
from .tasks import set_ptice, set_comment
from .recievers import delete_cache_total_sum


class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args,  **kwargs):
        if self.__full_price != self.full_price:
            for subscription in self.subscriptions.all():
                set_ptice.delay(subscription.id)
                set_comment.delay(subscription.id)

        return super().save(*args, **kwargs)


class Plan(models.Model):
    PLAN_TYPES = (
        ("full", "Full"),
        ("student", "Student"),
        ("discount", "Discount"),
    )

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def save(self, *args,  **kwargs):
        if self.__discount_percent != self.discount_percent:
            for subscription in self.subscriptions.all():
                set_ptice.delay(subscription.id)
                set_comment.delay(subscription.id)

        return super().save(*args, **kwargs)





class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name="subscriptions", on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name="subscriptions", on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name="subscriptions", on_delete=models.PROTECT)
    price = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=50, default='', db_index=True)

    fiald_a = models.CharField(max_length=50, default='')
    fiald_b = models.CharField(max_length=50, default='')

    class Meta:
        indexes = [
            models.Index(fields=['fiald_a', 'fiald_b'])
        ]


    def save(self, *args,  **kwargs):
        response = super().save(*args, **kwargs)
        creating = not bool(not self.id)
        if creating:
            set_ptice.delay(self.id)

        return response


post_delete.connect(delete_cache_total_sum, sender=Subscription)