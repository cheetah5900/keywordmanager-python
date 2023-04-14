# Generated by Django 3.2 on 2023-04-13 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0023_auto_20230329_0753'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempLinkOfWorkModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.RenameModel(
            old_name='TempListOfWorkModel',
            new_name='ListOfHouseModel',
        ),
        migrations.RenameModel(
            old_name='TempListOfHouseModel',
            new_name='ListOfWorkModel',
        ),
    ]
