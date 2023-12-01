# Generated by Django 4.2.7 on 2023-12-01 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('title', models.TextField(default='Sin título', max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('response', models.TextField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]