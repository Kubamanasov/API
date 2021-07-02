from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework

from .models import Product, Review, LikeList, Favorite, Cart
from .filters import ProductFilter
from .permissions import IsAuthorOrAdmin, Ban
from .serializers import ProductListSerializer, ProductDetailSerializer, ReviewSerializer, \
    LikeSerializer, FavoriteListSerializer, CartListSerializer


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    filter_backends = (rest_framework.DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ['title', 'price']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        elif self.action in ['create_review', 'like', 'favorites', 'cart']:
            return [IsAuthenticated()]
        return []

    @action(detail=True, methods=['POST'])
    def create_review(self, request, pk):  # в pk прилетает id продукта
        data = request.data.copy()
        data['product'] = pk
        serializer = ReviewSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):   # raise_exeption=True - это выдает нам правильную ошибку при случии его выявление для того что бы мы могли испровить
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    # /api/v1/products/id/like
    @action(detail=True, methods=['POST'])
    def like(self, request, pk):
        product = self.get_object()
        user = request.user
        like_obj, created = LikeList.objects.get_or_create(product=product, user=user)
        if like_obj.is_liked:
            like_obj.is_liked = False
            like_obj.save()
            return Response('dislike')
        else:
            like_obj.is_liked = True
            like_obj.save()
            return Response('like')

    @action(detail=True, methods=['POST'])
    def favorite(self, request, pk):
        product = self.get_object()
        user = request.user
        favorit, created = Favorite.objects.get_or_create(product=product, user=user)
        if favorit.favorite:
            favorit.favorite = False
            favorit.save()
            return Response('Добавлено в избранное')
        else:
            favorit.favorite = True
            favorit.save()
            return Response('Убрано с Избранных')

    @action(detail=True, methods=['POST'])
    def cart(self, request, pk):
        product = self.get_object()
        user = request.user
        cart, created = Cart.objects.get_or_create(product=product, user=user)
        if cart.add:
            cart.add = False
            cart.save()
            return Response('Добавлено в Карзину')
        else:
            cart.add = True
            cart.save()
            return Response('Убрано с карзины')

    @action(detail=False, methods=['get'])  # для чего нам нужен action -> router builds path posts/search
    def search(self, request, pk=None):
        q = request.query_params.get('q')  # request.query_params = request.GET
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        serializer = ProductDetailSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), ]
        else:
            return [IsAuthorOrAdmin]


class LikeViewSet(viewsets.ModelViewSet):

    queryset = LikeList.objects.all()
    serializer_class = LikeSerializer


# class OrderViewSet(viewsets.ModelViewSet):
#
#     queryset = Order.objects.all()
#     serializer_class = OrderItemSerializer
#     filter_backends = (rest_framework.DjangoFilterBackend, OrderingFilter)
#     filterset_class = OrderFilter
#     ordering_fields = ['total_sum', 'created_at']
#
#     def get_permissions(self):
#         if self.action in ['create', 'list', 'retrieve']:
#             return [IsAuthenticated()]
#         elif self.action in ['update', 'partial_update']:
#             return [IsAuthenticated()]
#         else:
#             return [Ban()]
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         if not self.request.user.is_staff:
#             queryset = queryset.filter(rider=self.request.rider)
#         return queryset


class Favorites(ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}


class CartProducts(ListAPIView):

    queryset = Cart.objects.all()
    serializer_class = CartListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}