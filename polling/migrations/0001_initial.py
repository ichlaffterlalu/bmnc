# Generated by Django 2.0 on 2018-05-20 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Polling',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('polling_start', models.DateTimeField()),
                ('polling_end', models.DateTimeField()),
                ('total_responden', models.IntegerField()),
            ],
            options={
                'db_table': 'polling',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PollingBerita',
            fields=[
                ('id_polling', models.ForeignKey(db_column='id_polling', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='polling.Polling')),
            ],
            options={
                'db_table': 'polling_berita',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PollingBiasa',
            fields=[
                ('id_polling', models.ForeignKey(db_column='id_polling', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='polling.Polling')),
                ('url', models.CharField(max_length=50)),
                ('deskripsi', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'polling_biasa',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Respon',
            fields=[
                ('id_polling', models.ForeignKey(db_column='id_polling', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='polling.Polling')),
                ('jawaban', models.CharField(max_length=50)),
                ('jumlah_dipilih', models.IntegerField()),
            ],
            options={
                'db_table': 'respon',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Responden',
            fields=[
                ('id_polling', models.ForeignKey(db_column='id_polling', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='polling.Polling')),
                ('ip_address', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'responden',
                'managed': False,
            },
        ),
    ]
