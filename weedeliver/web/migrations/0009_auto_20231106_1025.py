# Generated by Django 3.1.4 on 2023-11-06 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_remove_karrito_unitateak'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='karrito',
            name='produktuak',
        ),
        migrations.CreateModel(
            name='KarritoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unitateak', models.IntegerField()),
                ('produktua', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.produktua')),
            ],
        ),
        migrations.AddField(
            model_name='karrito',
            name='karrito_itemak',
            field=models.ManyToManyField(to='web.KarritoItem'),
        ),
    ]
