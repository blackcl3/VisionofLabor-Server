# Generated by Django 4.1.3 on 2023-02-22 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('value', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Chore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('frequency', models.CharField(max_length=50)),
                ('priority', models.CharField(max_length=50)),
                ('photo_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Household',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('photo_url', models.CharField(max_length=200)),
                ('admin', models.BooleanField()),
                ('household', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='visionoflaborapi.household')),
            ],
        ),
        migrations.CreateModel(
            name='ChoreCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visionoflaborapi.category')),
                ('chore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visionoflaborapi.chore')),
            ],
        ),
        migrations.AddField(
            model_name='chore',
            name='household',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='visionoflaborapi.household'),
        ),
        migrations.AddField(
            model_name='chore',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='visionoflaborapi.user'),
        ),
    ]
