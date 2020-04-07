# Generated by Django 2.1.7 on 2020-04-03 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.PositiveIntegerField(default=160)),
                ('male', models.BooleanField(default=False)),
                ('website', models.URLField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mysite.User')),
            ],
        ),
    ]