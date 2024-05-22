from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from products.models import Product

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên đăng nhập'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mât khẩu'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Xác nhận mật khẩu'})

class HistoryManager(models.Manager):
    def filter_by_products(self, product1_id, product2_id, account_id):
        queryset1 = self.filter(product1_id=product1_id, product2_id=product2_id, account_id=account_id)
        queryset2 = self.filter(product1_id=product2_id, product2_id=product1_id, account_id=account_id)
        return queryset1.union(queryset2)

class History(models.Model):
    id = models.AutoField(primary_key=True)
    account_id = models.CharField(max_length=100)
    product1 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product1')
    product2 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product2')
    time = models.DateTimeField(auto_now_add=True)

    objects = HistoryManager()  # Sử dụng custom manager

    def __str__(self):
        return self.product1.product_name + ' - ' + self.product2.product_name

    class Meta:
        db_table = 'history'
        managed = True
    
class SavedHistory(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    account_id = models.CharField(max_length=100)
    product1 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='saved_product1')
    product2 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='saved_product2')
    time = models.DateTimeField(auto_now_add=True)
    
    objects = HistoryManager()  # Sử dụng custom manager
    
    def __str__(self):
        return self.product1.product_name + ' - ' + self.product2.product_name

    class Meta:
        db_table = 'saved_history'
        managed = True