from django.contrib import admin

# Register your models here.
from .models import TaggedItem


class TaggedItemAdmin(admin.ModelAdmin):
    fields = ['tag', 'content_type', 'object_id', 'content_object']
    readonly_fields = ['content_object']

    class Meta:
        models = TaggedItem


admin.site.register(TaggedItem, TaggedItemAdmin)
