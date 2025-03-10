from django.contrib import admin

from shopapp.models import Order, Product


# Кастомизация отображения товаров в админке
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'is_available', 'created_at', 'orders_display')
    search_fields = ('name', 'price')
    actions = ['archive_products', 'not_archive_products']  # Добавляем групповое действие

    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        ('Цена', {'fields': ('price', 'quantity')}),
        ('Дополнительные опции', {'fields': ('is_available',), 'classes': ('collapse',)}),
    )

    # Отображение связи "ко многим" – список заказов с этим продуктом
    def orders_display(self, obj):
        return ", ".join([str(order.id) for order in obj.orders.all()])

    orders_display.short_description = "Заказы"

    # Функция для группового действия – архивирование товаров
    @admin.action(description="Архивировать выбранные товары")
    def archive_products(modeladmin, request, queryset):
        queryset.update(is_available=False)  # Делаем товары недоступными

    @admin.action(description='Разархивировать выбранные топары')
    def not_archive_products(modeladmin, request, queryset):
        queryset.update(is_available=True)


# Кастомизация отображения заказов в админке
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    list_filter = ('status',)  # Фильтрация по статусу заказов


# Регистрируем кастомные админ-классы
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
