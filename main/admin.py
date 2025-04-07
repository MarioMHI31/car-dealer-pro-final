from django.contrib import admin
from .models import Car, CarImage, Profile
from django.utils.html import format_html


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price', 'seller', 'featured', 'preview_main_image')
    list_filter = ('featured', 'brand', 'year', 'fuel_type', 'car_body')
    search_fields = ('brand', 'model', 'description', 'location')
    list_editable = ('featured',)
    readonly_fields = ('preview_main_image',)
    inlines = [CarImageInline]

    def preview_main_image(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" width="120" style="border-radius:6px;"/>', obj.main_image.url)
        return "Nicio imagine"
    preview_main_image.short_description = "Imagine"


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'preview_image')

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius:6px;"/>', obj.image.url)
        return "Fără imagine"
    preview_image.short_description = "Imagine"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'age', 'address')
    search_fields = ('user__email', 'user__username', 'phone')


