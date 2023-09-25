from django import forms
from .models import Produk, Status, Kategori

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['nama_produk', 'harga', 'kategori_id', 'status_id']

        widgets = {
            'nama_produk': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'harga': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'kategori_id': forms.Select(attrs={
                'class': 'form-control',
            }),
            'status_id': forms.Select(attrs={
                'class': 'form-control',
            })
        }

    