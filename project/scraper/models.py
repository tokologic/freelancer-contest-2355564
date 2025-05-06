from django.db import models


class AssetProperty(models.Model):

    name = models.CharField(max_length=255)
    cover_image_url = models.CharField(null=True, max_length=255)
    price = models.FloatField(null=True)
    city = models.CharField(null=True, max_length=255)
    kind = models.CharField(null=True, max_length=255)
    contact_name = models.CharField(null=True, max_length=255)
    company = models.CharField(null=True, max_length=255)
    summary = models.TextField(null=True, max_length=255)

    class Meta:
        db_table = "asset_properties"
