from django.db import models
from utils.resizing import resize_image
from utils.rands import slugify_new
from utils.omfilters import formata_preco
# from utils.price_format import

# Create your models here.


class Product(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=255)
    long_description = models.TextField()
    image = models.ImageField(
        upload_to='product/images/%Y/%m',
        blank=True,
        null=True
    )
    slug = models.SlugField(
        unique=True,
        blank=True, null=True
    )
    marketing_price = models.FloatField(verbose_name='Price')
    marketing_price_promotion = models.FloatField(
        default=0, verbose_name='Price Promo.')
    type = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variable'),
            ('S', 'Simple'),
        )
    )

    def get_price_formated(self):
        return formata_preco(self.marketing_price)
    get_price_formated.short_description = 'Price'

    def get_price_promotional_formated(self):
        return formata_preco(self.marketing_price_promotion)
    get_price_promotional_formated.short_description = 'Price Promo.'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)

        # senao tiver ele nao guard pq é sobreescrito o metodo
        super_save = super().save(*args, **kwargs)
        max_image_size = 800
        if self.image:
            resize_image(self.image, max_image_size)

        return super_save

    def __str__(self) -> str:
        return self.name

# example: shirt can be for men or women, different sizes, colors
# so variation can be size, color, etc
# portanto, na vdd vendemos a variacao e nao o produto em si!


class Variation(models.Model):
    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'
    name = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField()
    promotion_price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=1)
    # 1 Produto - many Variation
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name or self.product.name
