from django.contrib import admin
from .models import Election, Candidate, Vote

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active', 'created_by')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'election')
    list_filter = ('election',)
    search_fields = ('name', 'position', 'bio')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'candidate', 'get_election', 'timestamp')
    list_filter = ('candidate__election', 'timestamp')
    search_fields = ('voter__email', 'candidate__name')
    date_hierarchy = 'timestamp'
    
    def get_election(self, obj):
        return obj.candidate.election
    get_election.short_description = 'Elección'
    get_election.admin_order_field = 'candidate__election'