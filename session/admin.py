from django.contrib import admin

from .models import CustomUser, ActivationCode , TeamMember, Designation


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name" , "last_name" , "username" , "email" , "user_type"]

    actions = ["mark_selected_user_as_teammate", "mark_selected_user_as_inactive"]

    @admin.action(description = "Mark selected user(s) as teammate")
    def mark_selected_user_as_teammate(self, request , queryset, **kwargs):
        count = queryset.update(user_type = "teammate")
        return self.message_user(request , message = f"Successfully marked {count} user as team mate")

    @admin.action(description = "Mark selected user(s) as inactive")
    def mark_selected_user_as_inactive(self, request , queryset, **kwargs):
        count = queryset.update(is_active = False)
        return self.message_user(request , message = f"Successfully marked {count} user as inactive")

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["user" , "designation", "started_from", "end_at", "is_active"]

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ["name" , "is_active"]

    actions = ["mark_selected_designation_as_active" , "mark_selected_designation_as_inactive"]

    @admin.action(description = "Mark selected designation(s) as active")
    def mark_selected_designation_as_active(self, request , queryset, **kwargs):
        count = queryset.update(is_active = True)
        return self.message_user(request , message = f"Successfully marked {count} designation as active")
    
    @admin.action(description = "Mark selected designation(s) as inactive")
    def mark_selected_designation_as_inactive(self, request , queryset, **kwargs):
        count = queryset.update(is_active = False)
        return self.message_user(request , message = f"Successfully marked {count} designation as inactive")

@admin.register(ActivationCode)
class ActivationCodeAdmin(admin.ModelAdmin):
    list_display =  ["user" , "code", "created_at", "expiry_date"]