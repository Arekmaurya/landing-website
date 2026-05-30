from django.contrib import admin
from django.utils.html import format_html
from .models import ClinicInformation, Credential, Review, Appointment

@admin.register(ClinicInformation)
class ClinicInformationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone', 'whatsapp', 'notification_method')
    readonly_fields = ('doctor_image_preview',)
    fieldsets = (
        ('Contact Info', {
            'fields': ('address', 'phone', 'whatsapp')
        }),
        ('Working Hours', {
            'fields': ('weekdays_working_hours', 'saturday_working_hours', 'sunday_working_hours')
        }),
        ('Location & Maps', {
            'fields': ('map_link',)
        }),
        ('Social Links', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url')
        }),
        ('Doctor Profile Image', {
            'fields': ('doctor_image_preview', 'doctor_image'),
            'description': 'Upload a profile photo for the About section. Max 2 MB. Accepted: .jpg, .jpeg, .png, .webp',
        }),
        ('Notification Settings', {
            'fields': ('notification_method',)
        }),
    )

    class Media:
        css = {'all': ('admin/css/admin_doctor_image.css',)}
        js = ('admin/js/admin_doctor_image.js',)

    def doctor_image_preview(self, obj):
        if obj.doctor_image:
            return format_html(
                '<div id="doctor-image-preview-container">'
                '<img src="{}" id="doctor-image-current" '
                'style="max-width: 200px; max-height: 200px; border-radius: 10px; '
                'object-fit: cover; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />'
                '</div>',
                obj.doctor_image.url
            )
        return format_html(
            '<div id="doctor-image-preview-container">'
            '<span style="color: #999; font-style: italic;">{}</span>'
            '</div>',
            'No image uploaded'
        )
    doctor_image_preview.short_description = 'Current Image'
    
    def has_add_permission(self, request):
        # Enforce singleton pattern (only 1 config allowed)
        if ClinicInformation.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Do not allow deletion of the core settings
        return False


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ('text', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'stars', 'avatar_preview', 'quote')
    list_filter = ('stars',)
    search_fields = ('name', 'quote')

    def avatar_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;" />', obj.image.url)
        return format_html('<span style="background: #187fb0; color: white; padding: 6px 8px; border-radius: 50%; font-weight: bold; font-size: 0.85rem;">{}</span>', obj.initial or (obj.name[0] if obj.name else ''))
    
    avatar_preview.short_description = 'Avatar'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'sex', 'contact', 'created_at', 'status')
    list_filter = ('status', 'created_at', 'sex')
    list_editable = ('status',)
    search_fields = ('name', 'contact')
    readonly_fields = ('name', 'age', 'sex', 'contact', 'created_at')
    ordering = ('-created_at',)

