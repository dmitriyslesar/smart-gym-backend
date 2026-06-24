from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Order, OrderItem
from .serializers import UserSerializer, OrderSerializer

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class RegApiView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'success': True,
                    'token': token.key,
                    'user_id': user.id,
                    'email': user.email,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthApiView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Такого пользователя не существует',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'success': True,
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
            }
        )

# Список заказов только для администратора
class OrderListApi(generics.ListAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

# Создание заказа пользователем из корзины
class CreateOrderApi(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        cart_items = request.data.get('cart', [])
        if not cart_items:
            return Response({"detail": "Корзина пуста"}, status=status.HTTP_400_BAD_REQUEST)
        
        total_price = 0
        for item in cart_items:
            price_clean = int(str(item.get('price')).replace(' ', ''))
            total_price += price_clean * int(item.get('quantity', 1))
        
        order = Order.objects.create(user=request.user, total_price=total_price)
        
        for item in cart_items:
            price_clean = int(str(item.get('price')).replace(' ', ''))
            OrderItem.objects.create(
                order=order,
                product_name=item.get('name'),
                quantity=int(item.get('quantity', 1)),
                price=price_clean
            )
        
        return Response({"success": True, "order_id": order.id}, status=status.HTTP_201_CREATED)

class DeleteOrderApi(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]