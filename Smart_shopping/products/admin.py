from django.contrib import admin
from .models import Product, Sentiment, ProductSpec
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_id', 'category_id', 'TGDD_product_link', 'FPT_product_link', 'image']
    list_filter = ['product_name']
    search_fields = ['product_name']

admin.site.register(Product, ProductAdmin)

class ProductSpecsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'color', 'screen', 'rear_camera', 'front_camera', 'OS_CPU', 'memory_storage', 'ket_noi', 'pin_sac', 'tien_ich', 'thongtin_chung']
    list_filter = ['id', 'product__product_name']  # Định nghĩa các trường khác trong ProductSpecs để lọc
    search_fields = ['product__product_name']  # Tìm kiếm theo các trường khác trong ProductSpecs và tên sản phẩm

admin.site.register(ProductSpec, ProductSpecsAdmin)

class SentimentAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'company_name', 'product_tgdd_link', 'fpt_link', 's_pin', 's_general', 's_service', 's_others']
    list_filter = ['product__product_name']
    search_fields = ['product__product_name']

    def company_name(self, obj):
        return obj.company_id.company_name

    def product_name(self, obj):
        return obj.product.product_name
    
    def product_tgdd_link(self, obj):
        return obj.product.TGDD_product_link

    def fpt_link(self, obj):
        return obj.product.FPT_product_link

    company_name.short_description = 'Company'
    product_name.short_description = 'Product'
    product_tgdd_link.short_description = 'TGDD Link'
    fpt_link.short_description = 'FPT Link'
    
admin.site.register(Sentiment, SentimentAdmin)