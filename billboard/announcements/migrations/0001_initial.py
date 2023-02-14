# Generated by Django 4.1.6 on 2023-02-10 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(choices=[('TA', 'Tanks'), ('HE', 'Healers'), ('DD', 'Damage Dealers'), ('TR', 'Traders'), ('GM', 'Guild Masters'), ('QG', 'Quest Givers'), ('SM', 'Smiths'), ('TN', 'Tanners'), ('PM', 'Potion Makers'), ('SC', 'Spell Casters')], max_length=2, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('is_new', models.BooleanField(default=True)),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='announcements.announcement')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='announcement',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='announcements.author'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='category',
            field=models.ManyToManyField(related_name='categories', to='announcements.category'),
        ),
    ]
