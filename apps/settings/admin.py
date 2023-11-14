# django
from django.contrib import admin
from django.http import HttpResponseRedirect

# local import
from .models import *
from mobile_shop_project.settings import DEVELOPMENT


@admin.register(UniqueIdConfig)
class UniqueIdConfigAdmin(admin.ModelAdmin):
    list_display = ('preview', 'status', 'type')
    list_filter = ('type', )


@admin.register(ShopInformation)
class ShopInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    class Meta:
        model = ShopInformation

    def changelist_view(self, request, extra_context=None):
        if not DEVELOPMENT:
            obj = self.Meta.model.objects.last()
            if obj:
                return HttpResponseRedirect("%s%s/change/" % (request.build_absolute_uri(), obj.id))
            else:
                return super(ShopInformationAdmin, self).changelist_view(request, extra_context)
        else:
            return super(ShopInformationAdmin, self).changelist_view(request, extra_context)

    def has_add_permission(self, request):
        return not self.Meta.model.objects.last() if not DEVELOPMENT else True


@admin.register(InvoiceConfiguration)
class InvoiceConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', )

    class Meta:
        model = InvoiceConfiguration

    def changelist_view(self, request, extra_context=None):
        if not DEVELOPMENT:
            obj = self.Meta.model.objects.last()
            if obj:
                return HttpResponseRedirect("%s%s/change/" % (request.build_absolute_uri(), obj.id))
            else:
                return super(InvoiceConfigurationAdmin, self).changelist_view(request, extra_context)
        else:
            return super(InvoiceConfigurationAdmin, self).changelist_view(request, extra_context)

    def has_add_permission(self, request):
        return not self.Meta.model.objects.last() if not DEVELOPMENT else True


admin.site.register(InvoicePDFTemplate)
