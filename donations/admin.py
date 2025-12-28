from django.contrib import admin
from .models import Donation, Receipt


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'story', 'amount', 'status', 'donation_date')
    list_filter = ('status', 'donation_date')
    search_fields = ('donor__username', 'story__title', 'transaction_id')
    ordering = ('-donation_date',)
    readonly_fields = ('donation_date', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role != 'admin':
            # Non-admins can only see their own donations
            qs = qs.filter(donor=request.user)
        return qs


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('donation', 'receipt_number', 'created_at')
    search_fields = ('receipt_number', 'donation__donor__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
