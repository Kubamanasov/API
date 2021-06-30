from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


User = get_user_model()


class Category(models.Model):

    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    size = models.FloatField()
    color = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products', blank=True, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['author', 'product']


class StatusChoices(models.TextChoices):

    new = ('new', 'Новый')
    done = ('done', 'выполнен')
    canceled = ('canceled', 'отменён')


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItems')
    status = models.CharField(max_length=25, choices=StatusChoices.choices)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItems(models.Model):

    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='order_items')
    qt = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['order', 'product']  # это запрет для повторного добавление


class LikeList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)

