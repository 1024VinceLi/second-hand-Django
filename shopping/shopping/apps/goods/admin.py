from django.contrib import admin
from django.contrib import admin

from .models import *
# Register your models here.

"""
注册goods应用中的模型类
"""
class SKUAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        from celery_tasks.html.tasks import generate_static_sku_detail_html
        generate_static_sku_detail_html.delay(obj.id)

class SKUSpecificationAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        from celery_tasks.html.tasks import generate_static_sku_detail_html
        generate_static_sku_detail_html.delay(obj.sku.id)

    def delete_model(self, request, obj):
        sku_id = obj.sku.id
        obj.delete()
        from celery_tasks.html.tasks import generate_static_sku_detail_html
        generate_static_sku_detail_html.delay(sku_id)



class SKUImageAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        from celery_tasks.html.tasks import generate_static_sku_detail_html
        generate_static_sku_detail_html.delay(obj.sku.id)
        # 设置 SKU 默认图片
        sku = obj.sku
        if not sku.default_image_url:
            sku.default_image_url = obj.image.url
            sku.save()

    def delete_model(self, request, obj):

        sku_id = obj.sku.id

        obj.delete()
        from celery_tasks.html.tasks import generate_static_sku_detail_html
        generate_static_sku_detail_html.delay(sku_id)








admin.site.register(GoodsCategory)
admin.site.register(GoodsChannel)
admin.site.register(Goods)
admin.site.register(Brand)
admin.site.register(GoodsSpecification)
admin.site.register(SpecificationOption)
admin.site.register(SKU)
admin.site.register(SKUSpecification)
# admin.site.register(SKUSpecificationAdmin)
admin.site.register(SKUImage)
# admin.site.register(SKUImageAdmin)

