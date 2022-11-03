# Generated by Django 3.2 on 2022-07-02 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0012_auto_20220702_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebListModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='pagelistmodel',
            name='website_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='keywordapp.weblistmodel'),
        ),
    ]