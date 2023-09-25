from django.urls import path
from .views import FetchDataFromAPIView, ProdukListView, ProdukCreateView, ProdukUpdateView, ProdukDeleteView

urlpatterns = [
    path('fetch-data/', FetchDataFromAPIView.as_view(), name='fetch-data'),
    path('daftar-produk/', ProdukListView.as_view(), name='daftar-produk'),
    path('tambah-produk/', ProdukCreateView.as_view(), name='tambah-produk'),
    path('ubah-produk/<int:pk>/', ProdukUpdateView.as_view(), name='ubah-produk'),
    path('hapus-produk/<int:pk>/', ProdukDeleteView.as_view(), name='hapus-produk')
]
