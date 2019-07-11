from django.contrib import admin
from django.contrib import admin

from .models import *
# Register your models here.

"""
注册goods应用中的模型类
"""

admin.site.register(GoodsCategory)
admin.site.register(GoodsChannel)
admin.site.register(Goods)
admin.site.register(Brand)
admin.site.register(GoodsSpecification)
admin.site.register(SpecificationOption)
admin.site.register(SKU)
admin.site.register(SKUSpecification)
admin.site.register(SKUImage)
