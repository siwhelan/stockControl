from django.db import models

from django.db import models


class Ingredient(models.Model):
    product_code = models.CharField(max_length=50)
    ingredient = models.CharField(max_length=50)
    price_per_pack = models.FloatField()
    pack_size = models.IntegerField()
    amount = models.IntegerField()
