from django import forms

from . import models


class EmployeeForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=models.Department.objects.all())

    class Meta:
        model = models.Employee
        fields = ['name', 'department', 'phone', 'email',
                  'designation', 'address', 'is_verified', 'is_active']


class StockForm(forms.ModelForm):
    # status = forms.CharField(choices=models.Stock.PRODUCT_STATUS)
    class Meta:
        model = models.Stock
        fields = ['product_name', 'quantity', 'price_per_unit', 'status',]


class ExpenseForm(forms.ModelForm):
    
    class Meta:
        model = models.Expense
        fields = [
            'supplier_name',
            'description',
            'amount',
            
        ]
