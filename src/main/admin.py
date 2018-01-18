from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe

from main.models import *


class EditLinkToInlineObject(object):
    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label, instance._meta.model_name), args=[instance.pk])
        if instance.pk:
            return mark_safe(u'<a href="{u}">Редактировать</a>'.format(u=url))
        else:
            return ''

    def characteristics(self, instance):
        if instance.pk:
            chrs = CharacteristicSP.objects.filter(service_point__id=instance.pk)
            text = ''
            for c in chrs:
                text += str(c.type) + ': ' + str(c.value1) + '<br>'
            return mark_safe(text)
        else:
            return ''


class AzsInline(admin.TabularInline):
    model = Azs
    exclude = ('address',)
    extra = 0


class PersonalAdmin(admin.ModelAdmin):
    inlines = [
        AzsInline,
    ]


class AzsGroupAdmin(admin.ModelAdmin):
    inlines = [
        AzsInline,
    ]


class CharacteristicSPInline(admin.TabularInline):
    model = CharacteristicSP
    exclude = ('description',)
    extra = 0


class ServicePointAdmin(admin.ModelAdmin):
    inlines = [
        CharacteristicSPInline,
    ]
    list_filter = ['azs', 'type']


class ServicePointInline(EditLinkToInlineObject, admin.TabularInline):
    model = ServicePoint
    fields = ['type', 'characteristics', 'edit_link', 'is_active']
    readonly_fields = ('type', 'characteristics', 'edit_link')
    exclude = ('description',)
    extra = 0


class AzsAdmin(admin.ModelAdmin):
    inlines = [
        ServicePointInline,
    ]
    search_fields = ['full_name']
    list_filter = ['azs_group']


admin.site.register(Azs, AzsAdmin)
# admin.site.register(Personal, PersonalAdmin)
# admin.site.register(AzsGroup, AzsGroupAdmin)
admin.site.register(ServicePoint, ServicePointAdmin)

class EmployeesAZKAdmin(admin.ModelAdmin):
    search_fields = ['person']
    list_filter = ['status', 'azk']
    filter_horizontal = ['permission']
    list_display = ('person', 'status', 'azk')

admin.site.register(EmployeesAZK, EmployeesAZKAdmin)
admin.site.register(Permission)
admin.site.register(Person)
admin.site.register(Position)

admin.site.register(TypeServicePoint)
admin.site.register(TypeCharacteristicSP)
admin.site.register(CharacteristicSP)
# admin.site.register(Invent)
