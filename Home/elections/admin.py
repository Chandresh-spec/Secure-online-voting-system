from django.contrib import admin
from .models import Election, Candidate, Party

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'state', 'village', 'status', 'start_time', 'end_time')
    list_filter = ('level', 'status', 'state')
    search_fields = ('title', 'state', 'village')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'election', 'party')
    list_filter = ('election', 'party')
    search_fields = ('name', 'election__title')
