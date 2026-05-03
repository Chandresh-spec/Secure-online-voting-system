from django.contrib import admin
from .models import User, OTP, VoterVerification, VoterRoll, VillageAdmin


@admin.register(VoterRoll)
class VoterRollAdmin(admin.ModelAdmin):
    list_display = ['voter_id', 'full_name', 'email', 'village', 'state', 'designated_role', 'is_registered']
    list_filter = ['state', 'designated_role', 'is_registered']
    list_editable = ['designated_role']
    search_fields = ['voter_id', 'full_name', 'email', 'mobile_number', 'village']
    readonly_fields = ['created_at', 'is_registered']
    ordering = ['state', 'village', 'full_name']
    list_per_page = 50
    actions = ['reset_registration_flag']

    def reset_registration_flag(self, request, queryset):
        updated = queryset.update(is_registered=False)
        self.message_user(request, f"{updated} voter(s) reset — they can re-register now.")
    reset_registration_flag.short_description = 'Reset registration flag (allow re-registration)'


@admin.register(VillageAdmin)
class VillageAdminModelAdmin(admin.ModelAdmin):
    list_display = ['admin_id', 'full_name', 'email', 'village', 'state', 'designated_role', 'is_registered']
    list_filter = ['state', 'designated_role', 'is_registered']
    list_editable = ['designated_role']
    search_fields = ['admin_id', 'full_name', 'email', 'mobile_number', 'village']
    readonly_fields = ['created_at', 'is_registered']
    ordering = ['state', 'village', 'full_name']
    list_per_page = 50
    actions = ['reset_registration_flag']

    def reset_registration_flag(self, request, queryset):
        updated = queryset.update(is_registered=False)
        self.message_user(request, f"{updated} admin(s) reset — they can re-register now.")
    reset_registration_flag.short_description = 'Reset registration flag (allow re-registration)'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'voter_id', 'role', 'state', 'is_verified']
    list_filter = ['role', 'is_verified', 'state']
    search_fields = ['email', 'first_name', 'last_name', 'voter_id']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'is_used', 'created_at', 'expires_at']
    list_filter = ['is_used']


def approve_verifications(modeladmin, request, queryset):
    for v in queryset:
        v.approve()
    modeladmin.message_user(request, f"{queryset.count()} verification(s) approved.")

approve_verifications.short_description = 'Approve selected verifications'


@admin.register(VoterVerification)
class VoterVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'submitted_voter_id', 'full_name_on_card', 'dob_on_card', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['user__email', 'submitted_voter_id', 'full_name_on_card']
    readonly_fields = ['created_at', 'updated_at']
    actions = [approve_verifications]
