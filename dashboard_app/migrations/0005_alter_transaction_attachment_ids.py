# Generated by Django 4.2.4 on 2024-04-01 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0004_remove_transaction_attachment_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='attachment_ids',
            field=models.TextField(blank=True, default=[], null=True, verbose_name='Pièce joint'),
        ),
    ]
