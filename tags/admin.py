from django.contrib import admin

# Register your models here.
from .models import TaggedItem


admin.site.register(TaggedItem)