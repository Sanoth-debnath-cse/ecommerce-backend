from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound

from productio.models import Category
from shopio.rest.serializers.category import PrivateCategoryListSerializer

from shared.permission import IsShopOwner


class PrivateCategoryListView(ListCreateAPIView):
    permission_classes = [IsShopOwner]
    serializer_class = PrivateCategoryListSerializer

    def get_queryset(self):
        return Category.objects.filter()


class PrivateCategoryDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsShopOwner]
    serializer_class = PrivateCategoryListSerializer

    def get_object(self):
        category_uid = self.kwargs.get("category_uid")
        try:
            return Category.objects.get(uid=category_uid)
        except Category.DoesNotExist:
            raise NotFound("Category does not exist")
