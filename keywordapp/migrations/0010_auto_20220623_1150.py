# Generated by Django 3.2 on 2022-06-23 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0009_auto_20220622_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='countkeywordmodel',
            name='page_list',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='keywordapp.pagelistmodel'),
        ),
        migrations.AlterField(
            model_name='countkeywordmodel',
            name='type',
            field=models.CharField(blank=True, default='paragraph of main keyword', max_length=255, null=True),
        ),
    ]
