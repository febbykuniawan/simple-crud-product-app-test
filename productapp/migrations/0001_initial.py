# Generated by Django 4.2.5 on 2023-09-23 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id_kategori', models.AutoField(primary_key=True, serialize=False)),
                ('nama_kategori', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id_status', models.AutoField(primary_key=True, serialize=False)),
                ('nama_status', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Produk',
            fields=[
                ('id_produk', models.AutoField(primary_key=True, serialize=False)),
                ('nama_produk', models.CharField(max_length=100)),
                ('harga', models.DecimalField(decimal_places=2, max_digits=10)),
                ('kategori_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productapp.kategori')),
                ('status_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productapp.status')),
            ],
        ),
    ]
