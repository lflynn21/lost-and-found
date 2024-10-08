# Generated by Django 4.2.4 on 2023-10-25 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_founditem_reward_remove_founditem_sub_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='founditem',
            old_name='description',
            new_name='item_description',
        ),
        migrations.AddField(
            model_name='location',
            name='drop_location_decription',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='new_hub',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=200),
        ),
    ]
