from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Order(models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True, null=True,
        # para relacao invertida/inversa - user.post_set.all() -> user.post_create_by.QUERYSET!
        related_name='user_order'
    )

    total = models.FloatField(verbose_name="Total")
    status = models.CharField(
        default='C',
        max_length=1,
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        )
    )

    def __str__(self) -> str:
        return f'Order: {self.pk}'


class ItemOrder(models.Model):  # o produto do pedido!
    class Meta:
        verbose_name = 'ItemOrder'
        verbose_name_plural = 'ItemOrders'

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)  # name of product
    product_id = models.PositiveIntegerField()
    variation = models.CharField(max_length=255)  # name of variation
    variation_id = models.PositiveIntegerField()
    price = models.FloatField()
    promotion_price = models.FloatField(default=0)  # talvez remova
    quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)  # caminho da imagem!!

    def __str__(self) -> str:
        return f'Item of {self.order}'
