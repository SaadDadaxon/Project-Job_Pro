from django.contrib import admin
from .models import ApplyJob, Jobs, Like


class ApplyJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'jobs', 'rezume', 'create_date')


admin.site.register(Jobs),
admin.site.register(Like),
admin.site.register(ApplyJob, ApplyJobAdmin),

