from django.contrib import admin
from .models import Vote, VoteRecord

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('vote_hash', 'election', 'candidate', 'cast_at')
    list_filter = ('election',)
    search_fields = ('vote_hash', 'candidate__name')

@admin.register(VoteRecord)
class VoteRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'election', 'created_at')
    list_filter = ('election',)
    search_fields = ('user__username', 'user__email', 'election__title')
