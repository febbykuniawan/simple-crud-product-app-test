from django.views import generic
from productapp.models import Produk

class HomeView(generic.ListView):
    model = Produk
    template_name = 'home.html'
    
    def get_queryset(self):
        # Mendapatkan kumpulan data produk berdasarkan nama_status dari model Produk
        return Produk.objects.filter(status_id__nama_status='bisa dijual')