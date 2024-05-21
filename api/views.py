from rest_framework import generics
from rest_framework.response import Response

from product.models import Product

from .serializers import CountSerializer, ProductSerializer
from .tasks import parsing_goods_selenium


class ListProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        else:
            return CountSerializer

    def post(self, request):
        serializer = CountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # celery task
        parsing_goods_selenium.delay(serializer.data['product_count'])

        return Response({'result': f'Парсинг начался. Кол-во: {serializer.data["product_count"]}'})


class ProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
