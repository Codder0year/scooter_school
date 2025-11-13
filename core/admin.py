from django.contrib import admin

from core.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'has_image', 'has_video')
    list_filter = ('date_posted',)
    search_fields = ('title', 'content')

    def has_image(self, obj):
        return bool(obj.image)

    has_image.boolean = True
    has_image.short_description = 'Изображение'

    def has_video(self, obj):
        return bool(obj.video)

    has_video.boolean = True
    has_video.short_description = 'Видео'