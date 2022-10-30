from django.contrib import admin
from .models import User, Rol
from django.contrib.auth.models import Group
from rest_framework.authtoken.admin import TokenAdmin
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm


class UserCreationForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    list_display = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'is_active','role')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'name', 'is_staff', 'is_active','role')}
            ),
        )

    filter_horizontal = ()

TokenAdmin.raw_id_fields = ['user']
admin.site.register(User, CustomUserAdmin)
admin.site.register(Rol)
admin.site.unregister(Group)
