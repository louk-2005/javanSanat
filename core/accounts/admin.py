#django files
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.forms import TextInput, Textarea
from django.utils.safestring import mark_safe

#your files
from .models import User, ContactInfo, SocialLink


class AccountsUserAdmin(UserAdmin):
    # نمایش تصویر در لیست کاربران
    list_display = (
        'image_tag',
        'username',
        'email',
        'role',
        'first_name',
        'last_name',
        'is_active',
        'date_joined',
        'last_login'
    )

    # فیلترهای پیشرفته
    list_filter = (
        'role',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
        'last_login'
    )

    # جستجوی گسترده
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number'
    )

    ordering = ('-date_joined',)
    list_per_page = 25
    readonly_fields = ('image_tag_preview',)

    # فیلدهای اصلی برای ویرایش کاربر
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone_number',
                'role',
                'image'
            )
        }),
        ('دسترسی‌ها', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        ('تاریخ‌های مهم', {
            'fields': ('last_login', 'date_joined')
        }),
        ('پیش‌نمایش تصویر', {
            'fields': ('image_tag_preview',),
            'classes': ('collapse',),
        }),
    )

    # فیلدهای ایجاد کاربر جدید
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'phone_number',
                'role',
                'password1',
                'password2',
                'image'
            )
        }),
    )

    # اکشن‌های سفارشی
    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} کاربر با موفقیت فعال شدند.',
            level='success'
        )

    activate_users.short_description = "فعال‌سازی کاربران انتخاب‌شده"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} کاربر با موفقیت غیرفعال شدند.',
            level='warning'
        )

    deactivate_users.short_description = "غیرفعال‌سازی کاربران انتخاب‌شده"

    # نمایش تصویر در لیست کاربران
    def image_tag(self, obj):
        if obj.image and obj.image.name != 'default.jpg':
            return mark_safe(
                f'<img src="{obj.image.url}" width="50" height="50" style="border-radius:50%; object-fit: cover;" />'
            )
        return mark_safe(
            '<img src="/media/default.jpg" width="50" height="50" style="border-radius:50%; object-fit: cover;" />'
        )

    image_tag.short_description = 'تصویر'
    image_tag.allow_tags = True

    # نمایش تصویر بزرگتر در فرم ویرایش
    def image_tag_preview(self, obj):
        if obj.image and obj.image.name != 'default.jpg':
            return mark_safe(
                f'<img src="{obj.image.url}" width="200" height="200" style="border-radius:10%; object-fit: cover;" />'
            )
        return mark_safe(
            '<img src="/media/default.jpg" width="200" height="200" style="border-radius:10%; object-fit: cover;" />'
        )

    image_tag_preview.short_description = 'پیش‌نمایش تصویر'
    image_tag_preview.allow_tags = True


admin.site.register(User, AccountsUserAdmin)




# Register your models here.

class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1
    fields = ('name', 'url')
    classes = ['collapse']

    def formfield_for_dbfield(self, db_field, **kwargs):
        # Customize form fields for better UI
        if db_field.name == 'name':
            kwargs['widget'] = TextInput(attrs={'class': 'vTextField', 'style': 'width: 200px;'})
        elif db_field.name == 'url':
            kwargs['widget'] = TextInput(attrs={'class': 'vTextField', 'style': 'width: 400px;'})
        return super().formfield_for_dbfield(db_field, **kwargs)


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1
    fields = ('name', 'url')
    classes = ['collapse']

    def formfield_for_dbfield(self, db_field, **kwargs):
        # Customize form fields for better UI
        if db_field.name == 'name':
            kwargs['widget'] = TextInput(attrs={'class': 'vTextField', 'style': 'width: 200px;'})
        elif db_field.name == 'url':
            kwargs['widget'] = TextInput(attrs={'class': 'vTextField', 'style': 'width: 400px;'})
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = (
    'get_name_display', 'phone_display', 'email_display', 'address_preview', 'logo_thumbnail', 'updated_at')
    list_filter = ('name', 'updated_at')
    search_fields = ('name', 'phone', 'email', 'address', 'description')
    readonly_fields = ('logo_thumbnail', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'logo', 'logo_thumbnail')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address'),
            'classes': ('collapse', 'open')
        }),
        ('Additional Information', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('updated_at',),
            'classes': ('collapse',),
            'description': 'System managed information'
        }),
    )
    inlines = [SocialLinkInline]

    def get_name_display(self, obj):
        return obj.get_name_display()

    get_name_display.short_description = 'نام شعبه'
    get_name_display.admin_order_field = 'name'

    def phone_display(self, obj):
        return obj.phone if obj.phone else '---'

    phone_display.short_description = 'تلفن'
    phone_display.admin_order_field = 'phone'

    def email_display(self, obj):
        return obj.email if obj.email else '---'

    email_display.short_description = 'ایمیل'
    email_display.admin_order_field = 'email'

    def address_preview(self, obj):
        if obj.address:
            return format_html(
                '<span title="{}">{}</span>',
                obj.address,
                (obj.address[:50] + '...') if len(obj.address) > 50 else obj.address
            )
        return '---'

    address_preview.short_description = 'آدرس'
    address_preview.admin_order_field = 'address'

    def logo_thumbnail(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />',
                obj.logo.url
            )
        return '---'

    logo_thumbnail.short_description = 'لوگو'
    logo_thumbnail.allow_tags = True

    def get_queryset(self, request):
        # FIXED: Use prefetch_related for reverse relationships
        return super().get_queryset(request).prefetch_related('social_links')

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url_display', 'contact_name', 'get_contact_name_display')
    list_filter = ('contact__name', 'name')
    search_fields = ('name', 'url', 'contact__name')
    # CORRECT: Use select_related for forward relationships
    list_select_related = ('contact',)

    def url_display(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.url,
            (obj.url[:30] + '...') if len(obj.url) > 30 else obj.url
        )

    url_display.short_description = 'لینک'
    url_display.allow_tags = True

    def contact_name(self, obj):
        return obj.contact.name

    contact_name.short_description = 'شعبه'
    contact_name.admin_order_field = 'contact__name'

    def get_contact_name_display(self, obj):
        return obj.contact.get_name_display()

    get_contact_name_display.short_description = 'نام شعبه'
    get_contact_name_display.admin_order_field = 'contact__name'

    fieldsets = (
        (None, {
            'fields': ('contact', 'name', 'url')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "contact":
            kwargs["queryset"] = ContactInfo.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }