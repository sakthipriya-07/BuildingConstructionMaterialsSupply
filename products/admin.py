from django.contrib import admin



from .models import Category, Product, RFQ


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created']
    list_filter = ['available', 'created']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(RFQ)
class RFQAdmin(admin.ModelAdmin):
    list_display = ['Category_Type', 'Brand', 'Material_description', 'Location', 'Attachment']
