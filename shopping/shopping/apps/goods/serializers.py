from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers

from goods.models import SKU
from goods.search_indexes import SKUIndex


class SKUIndexSerializer(HaystackSerializer):
    """
    SKU索引结果序列化器
    """

    class Meta:
        index_class = [SKUIndex]
        fields = ('text','id','name','price','default_image_url','comments')


class SKUSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKU
        fields = {'id','name','price','default_image_url','comments'}