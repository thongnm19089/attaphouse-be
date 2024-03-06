from django.db import models
import uuid
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from .color import Color
from .brand import Brand
from ...categories.models import SubCategory
from ...uploads.models import File
from django.db.models import Q
from ...tags.models import Tag
from ...sizes.models import Size

class Product(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50)
    url = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    price_new = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    price_old = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    quantity = models.IntegerField(default=0)
    coupon = models.CharField(max_length=50, blank=True)
    size = models.ManyToManyField(Size, related_name="products", blank=True)
    STATUS_CHOICES = (
        ('Published', 'Published'),
        ('Scheduled', 'Scheduled'),
        ('Hidden', 'Hidden'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Published')
    publish_time = models.DateTimeField(blank=True, null=True)
    image = models.ForeignKey(File, on_delete=models.SET_NULL, related_name="product_image", null=True)
    sub_image = models.ManyToManyField(File, blank=True, related_name="product_sub_image")
    tag = models.ManyToManyField(Tag, related_name="products", blank=True)
    sub_category = models.ManyToManyField(SubCategory, related_name="products", blank=True)
    color = models.ManyToManyField(Color, related_name="products", blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, related_name="products", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product"
        constraints = [
            models.UniqueConstraint(
                fields=["url"], 
                name="unique_product_url", 
                condition=Q(deleted__isnull=True)
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return '{}'.format(self.name)