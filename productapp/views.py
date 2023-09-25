from django.shortcuts import redirect
import requests, hashlib
from datetime import datetime
from .models import Kategori, Status, Produk
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as drf_status
from django.urls import reverse_lazy
from .forms import ProdukForm
import pytz
import hashlib

def generate_username_and_password():
    # Mendapatkan tanggal dan waktu saat ini
    now = datetime.now()

    # Mengatur timezone ke GMT+8 (Asia/Singapore)
    gmt8_tz = pytz.timezone('Asia/Singapore')
    now = now.astimezone(gmt8_tz)  # Mengubah ke timezone Asia/Singapore

    # Mengambil jam saat ini dengan format HH (24 jam) dan memastikan dua digit
    formatted_hour = now.strftime("%H").zfill(2)
    # Mengambil tanggal dengan format DDMMYY
    formatted_date = now.strftime("%d%m%y")

    # Pembentukan username dengan format "tesprogrammerDDMMYYCHH"
    username = f"tesprogrammer{formatted_date}C{formatted_hour}"
    # Pembentukan password dengan format "bisacoding-DD-MM-YY"
    password = f"bisacoding-{now.day:02d}-{now.month:02d}-{str(now.year)[-2:]}"

    # Hashing password menggunakan MD5
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    # Mengembalikan username dan hashed password
    return username, hashed_password
        
class FetchDataFromAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Menghasilkan nama pengguna (username) dan kata sandi terenkripsi
        username, password = generate_username_and_password()
        
        # Persiapkan payload untuk permintaan ke API
        payload = {
            'username': username,
            'password': password
        }

        # URL endpoint API untuk mengambil data
        api_url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
        
        # Kirim permintaan POST ke API dengan payload
        response = requests.post(api_url, data=payload)
        
        # Periksa apakah permintaan API berhasil (kode status 200)
        if response.status_code == 200:
            # Parse data respons sebagai JSON dan ambil bagian 'data'
            data = response.json()['data']

            # Iterasi data yang diperoleh dari API
            for item in data:
                # Periksa apakah produk dengan nama yang sama sudah ada
                existing_produk = Produk.objects.filter(nama_produk=item['nama_produk']).first()

                # Perbarui produk jika ada dan harganya berbeda
                if existing_produk:
                    if existing_produk.harga != item['harga']:
                        existing_produk.harga = item['harga']
                        existing_produk.save()
                else:
                    # Buat produk baru jika belum ada
                    kategori, _ = Kategori.objects.get_or_create(nama_kategori=item['kategori'])
                    status, _ = Status.objects.get_or_create(nama_status=item['status'])

                    Produk.objects.create(
                        nama_produk=item['nama_produk'],
                        harga=item['harga'],
                        kategori_id=kategori,
                        status_id=status
                    )

            # Redirect ke halaman daftar produk
            return redirect('daftar-produk')
        else:
            # Mengembalikan respons error jika permintaan API gagal
            return Response({"error": "Gagal mengambil data dari API."}, status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProdukListView(ListView):
    model = Produk
    template_name = 'produk_index.html'
    paginate_by = 10
    success_url = reverse_lazy('daftar-produk')

    def get_queryset(self):
        # Mendapatkan kumpulan data produk dari model Produk
        return Produk.objects.all()

class ProdukCreateView(CreateView):
    model = Produk
    form_class = ProdukForm
    template_name = 'produk_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Set nilai kategori_id dan status_id dari instance form
        form.instance.kategori_id = form.cleaned_data['kategori_id']
        form.instance.status_id = form.cleaned_data['status_id']

        # Memanggil method form_valid dari parent class untuk melanjutkan proses validasi form
        return super().form_valid(form)

class ProdukUpdateView(UpdateView):
    model = Produk
    form_class = ProdukForm
    template_name = 'produk_update.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Memanggil method form_valid dari parent class untuk melanjutkan proses validasi form
        return super().form_valid(form)

class ProdukDeleteView(DeleteView):
    model = Produk
    success_url = reverse_lazy('daftar-produk')

    def post(self, request, *args, **kwargs):
        # Memanggil method delete menggunakan metode HTTP POST
        return self.delete(request, *args, **kwargs)