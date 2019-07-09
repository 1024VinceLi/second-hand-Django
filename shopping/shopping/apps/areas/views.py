from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Area
from .serializers import AreaSerializer, SubAreaSerializer


class AreasViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    行政区划信息
    """
    pagination_class = None # 区域划分不分页(禁止分页)

    def get_queryset(self):
        """
        提供数据集
        :return:
        """
        if self.action == 'list':
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()

    def get_serializer_class(self):
        """
        提供序列化器
        :return:
        """
        if self.action == 'list':
            return AreaSerializer
        else:
            return SubAreaSerializer
        