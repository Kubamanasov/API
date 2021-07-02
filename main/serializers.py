from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Product, Review, LikeList, Favorite, Cart

User = get_user_model()


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:

        model = Product
        fields = ('id', 'title', 'price', 'image')


class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:

        model = Product
        fields = '__all__'

    def get_rating(self, instance):
        total_rating = sum(instance.reviews.values_list('rating', flat=True))
        reviews_count = instance.reviews.count()
        rating = total_rating / reviews_count if reviews_count > 0 else 0
        return round(rating, 1)

    def get_like(self, instance):
        total_count = sum(instance.likes.values_list('is_liked', flat=True))
        likes = total_count if total_count > 0 else 0
        return likes

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        rep['rating'] = self.get_rating(instance)
        rep['like'] = self.get_like(instance)
        return rep


class FavoriteDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class CartDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ReviewAuthorSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('name', 'surname')

    def to_representation(self, instance):   # ////////////////////////////////////////////////////////////////
        representation = super().to_representation(instance)
        if not instance.name and instance.surname:
            representation['full_name'] = 'Анонимный пользователь'
        return representation


class LikeSerializer(serializers.ModelSerializer):

    class Meta:

        model = LikeList
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['author'] = LikeSerializer(instance.author).data
        return rep


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:

        model = Review
        exclude = ('author', 'id')

    def validate_rating(self, rating): #проверка рейтинга что он от 1 до 5
        if not rating in range(1, 6):
            raise serializers.ValidationError('Рейтинг должен быть от 1 до 5')
        return rating

    def validate(self, attrs):  # это метод для того что бы тот кто загружает пост стал его автором
        request = self.context.get('request')
        attrs['author'] = request.user
        return attrs

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['author'] = ReviewAuthorSerializer(instance.author).data
        return rep

#
# class OrderItemSerializer(serializers.ModelSerializer):
#
#     class Meta:
#
#         model = Product
#         fields = '__all__'
#
#
# class OrderSerializer(serializers.ModelSerializer):
#
#     # products = OrderItemSerializer(many=True)
#
#     class Meta:
#
#         model = OrderItems
#         fields = '__all__'
#
#     def create(self, validated_data):
#         total_sum = 0
#         request = self.context.get('request')  # берем запрос
#         validated_data['user'] = request.user  # с запроса берем и делаем юзера
#         validated_data['status'] = 'new'  # заказу задаем статус ню
#         validated_data['total_sum'] = total_sum
#         products = validated_data.pop('products')
#         order = Order.objects.create(**validated_data)  # создаем с этими данными заказ
#         for prod in products:
#             total_sum += prod['qt'].price * prod['qt']
#             OrderItems.objects.create(order=order, **prod)
#         order.total_sum = total_sum
#         order.save()
#         return order
#
#     def to_representation(self, instance):
#         rep = super().to_representation(instance)
#         rep['author'] = OrderItemSerializer(instance.author).data
#         return rep


class FavoriteListSerializer(serializers.ModelSerializer):

    class Meta:

        model = Favorite
        exclude = ('id', 'favorite', 'user')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = FavoriteDetailsSerializer(Product.objects.filter(favorite=instance.id), many=True, context=self.context).data
        return representation


class CartListSerializer(serializers.ModelSerializer):

    class Meta:

        model = Cart
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = CartDetailsSerializer(Product.objects.filter(cart=instance.id), many=True, context=self.context).data
        return representation
