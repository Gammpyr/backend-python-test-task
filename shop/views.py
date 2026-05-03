from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Category, Product, Cart, CartItem
from shop.pagination import ShopPagination
from shop.serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = ShopPagination
    permission_classes = [AllowAny]  # TODO - указать права доступа


class ProductViewSet(viewsets.ModelViewSet):
    """Продукты"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ShopPagination
    permission_classes = [AllowAny]  # TODO - указать права доступа


class CartViewSet(viewsets.ModelViewSet):
    """Корзина"""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]  # TODO - указать права доступа

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    """Товары в корзине"""
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]  # TODO - указать права доступа


class UpdateCartItemView(APIView):
    """Изменение количества товара в корзине

    {
        "product": 5,
        "quantity": 3, #необязательно
        "increase": true, #необязательно
        "decrease": true #необязательно
    }

    Если количество станет равно нулю или меньше, то товар удаляется из карточки
    """
    permission_classes = [IsAuthenticated]  # TODO - указать права доступа

    def post(self, request):
        user = request.user

        product_id = request.data.get('product')
        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get("quantity", 1)
        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return Response({'error': 'Неверное значение quantity'}, status=status.HTTP_400_BAD_REQUEST)

        increase_q = request.data.get('increase', False)
        decrease_q = request.data.get('decrease', False)

        cart, _ = Cart.objects.get_or_create(user=user)

        cart_item, created_item = CartItem.objects.get_or_create(
            cart_id=cart,
            product_id=product,
            defaults={"quantity": quantity if quantity > 0 else 1}
        )

        cur_quantity = cart_item.quantity
        if not created_item:
            if decrease_q:
                cur_quantity -= 1
            elif increase_q:
                cur_quantity += 1
            else:
                cur_quantity += quantity

            if cur_quantity <= 0:
                cart_item.delete()
                return Response(
                    {
                        'message': f'Товар {product.name} удален из корзины',
                    }
                )
            else:
                cart_item.quantity = cur_quantity
            cart_item.save()

        return Response({
            'message': f'Количество товара {product.name} изменено',
            'quantity': cart_item.quantity,
            'total_price': cart.total_price()
        }, status=status.HTTP_200_OK)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        cart_obj, _ = Cart.objects.get_or_create(user=user)

        cart_data = []
        for item in cart_obj.cart_items.all():
            cart_data.append({
                "id": item.id,
                "product_id": item.product_id.pk,
                "product_name": item.product_id.name,
                "quantity": item.quantity,
                "total_price": item.total_price_item_cart()
            })

        return Response(cart_data)
