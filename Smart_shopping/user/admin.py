from django.contrib import admin
from .models import History, SavedHistory

class HistoryAdmin(admin.ModelAdmin):
    def str_display(self, obj):
        return str(obj)  # Sử dụng phương thức __str__ của mô hình History

    str_display.short_description = 'History'  # Đặt tên cho cột hiển thị

    list_display = ['str_display', 'time']
    list_filter = ['time']
    search_fields = ['product1__product_name', 'product2__product_name', 'account__username']
    ordering = ['-time']
    
admin.site.register(History, HistoryAdmin)

class SavedHistoryAdmin(admin.ModelAdmin):
    def str_display(self, obj):
        return str(obj)  # Sử dụng phương thức __str__ của mô hình SavedHistory

    str_display.short_description = 'History'  # Đặt tên cho cột hiển thị

    list_display = ['str_display']  # Chỉ sử dụng trường str_display
    search_fields = ['product1__product_name', 'product2__product_name']  # Sử dụng các trường tìm kiếm thích hợp
    ordering = ['-id']  # Sắp xếp theo trường id hoặc trường nào khác trong SavedHistory

admin.site.register(SavedHistory, SavedHistoryAdmin)