from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image', 'stock']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step':'0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }