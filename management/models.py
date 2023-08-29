from django.db.models import Max
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from customer.models import Customer
from dashboard.models import Hotel

INVOICE_STATUS = [
    ('pending', 'في الانتظار'),
    ('complete', 'مكتملة'),
    ('cancelled', 'ملغية'),
]


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=INVOICE_STATUS, default='pending')
    payment_date = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return str(self.invoice_number)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.description


def generate_invoice_number(instance):
    last_invoice = Invoice.objects.all().aggregate(Max('invoice_number'))['invoice_number__max']
    if last_invoice:
        new_invoice_number = int(last_invoice.split('-')[1]) + 1
    else:
        new_invoice_number = 1
    return f'inv-{new_invoice_number:05d}'


@receiver(pre_save, sender=Invoice)
def set_invoice_number(sender, instance, **kwargs):
    if not instance.invoice_number:
        instance.invoice_number = generate_invoice_number(instance)
