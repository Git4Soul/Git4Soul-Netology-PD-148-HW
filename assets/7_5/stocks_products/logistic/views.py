from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['products']
    search_fields = ['address']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Дополнительный поиск (для доп. задания)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(products__title__icontains=search) | \
                       queryset.filter(products__description__icontains=search)
        return queryset.distinct()