from django.db.models import Max
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from customer.models import Customer
from dashboard.models import Hotel


class Invoice(models.Model):

    INVOICE_STATUS = [
        ('pending', 'في الانتظار'),
        ('complete', 'مكتملة'),
        ('cancelled', 'ملغية'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=INVOICE_STATUS, default='pending')
    payment_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    
    # processing_fee
    def __str__(self):
        return str(self.invoice_number)

    # def save(self, *args, **kwargs):
    #     # Calculate the total amount by summing up the amounts of related InvoiceItems
    #     self.total_amount = self.items.aggregate(total=models.Sum('amount'))['total'] or 0
        
    #     super().save(*args, **kwargs)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        return float(self.unit_price * self.quantity)


    def __str__(self):
        return self.description


def generate_invoice_number(instance):
    last_invoice = Invoice.objects.all().aggregate(Max('invoice_number'))['invoice_number__max']
    if last_invoice:
        new_invoice_number = int(last_invoice.split('-')[1]) + 1
    else:
        new_invoice_number = 1
    return f'INV-{new_invoice_number:05d}'


@receiver(pre_save, sender=Invoice)
def set_invoice_number(sender, instance, **kwargs):
    if not instance.invoice_number:
        instance.invoice_number = generate_invoice_number(instance)


class Stock(models.Model):
    PRODUCT_STATUS = (
        ('in_stock', 'متوفر'),
        ('out_of_stock', 'إنتهى المخزون'),
        ('low', 'منخفض'),
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PRODUCT_STATUS, default='in_stock')
    stock_number = models.CharField(
        max_length=10,
        unique=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        if self.quantity and self.price_per_unit:
            return self.quantity * self.price_per_unit
        return 0

    def __str__(self):
        return self.product_name

def generate_stock_number(instance):
    last_stock = Stock.objects.all().aggregate(Max('stock_number'))['stock_number__max']
    if last_stock:
        new_stock_number = int(last_stock.split('-')[1]) + 1
    else:
        new_stock_number = 1
    return f'STK-{new_stock_number:05d}'

@receiver(pre_save, sender=Stock)
def set_stock_number(sender, instance, **kwargs):
    if not instance.stock_number:
        instance.stock_number = generate_stock_number(instance)


class Department(models.Model):
    name = models.CharField(max_length=50)
    hotel = models.ForeignKey(to=Hotel, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def total_employee(self):
        return self.employee_set.count()

    def __str__(self) -> str:
        return self.name


class Employee(models.Model):

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone = models.CharField(max_length=32)
    email = models.EmailField()
    designation = models.CharField(max_length=200)
    address = models.CharField(max_length=250)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Expense(models.Model):
    expense_number = models.CharField(
        max_length=10,
        unique=True,
        blank=True
    )
    hotel = models.ForeignKey(to=Hotel, on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.description

def generate_expense_number(instance):
    last_expense = Expense.objects.all().aggregate(Max('expense_number'))['expense_number__max']
    if last_expense:
        new_expense_number = int(last_expense.split('-')[1]) + 1
    else:
        new_expense_number = 1
    return f'EXP-{new_expense_number:05d}'

@receiver(pre_save, sender=Expense)
def set_expense_number(sender, instance, **kwargs):
    if not instance.expense_number:
        instance.expense_number = generate_expense_number(instance)

