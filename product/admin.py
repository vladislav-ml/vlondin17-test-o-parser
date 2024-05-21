from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description_short', 'image_url', 'discount')
    list_display_links = ('id', 'name')

    def description_short(self, object):
        if object.description:
            if len(object.description) > 10:
                return ' '.join(object.description.split()[:15]) + ' ...'
        return '-'


admin.site.register(Product, ProductAdmin)
