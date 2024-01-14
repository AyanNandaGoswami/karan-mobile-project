from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import F, FloatField, ExpressionWrapper, Q, Sum


class PaymentStatusFilter(admin.SimpleListFilter):
    title = _('Payment Status')
    parameter_name = 'payment_status'

    def lookups(self, request, model_admin):
        return (
            ('due', _('Due')),
            ('no_due', _('No Due')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'due':
            queryset = queryset.prefetch_related('invoice_items').annotate(invoice_total_amt=Sum(F('invoice_items__cost'))).filter(
                invoice_total_amt__gt=0, finance__isnull=True)
            print(queryset)

            return queryset.annotate(due=ExpressionWrapper(F('invoice_total') - F('paid_amount'), output_field=FloatField())).filter(
                due__gt=0, finance__isnull=True)
        elif self.value() == 'no_due':
            return queryset.annotate(due=ExpressionWrapper(F('invoice_total') - F('paid_amount'), output_field=FloatField())).filter(
                Q(finance__isnull=False) | Q(due=0))



