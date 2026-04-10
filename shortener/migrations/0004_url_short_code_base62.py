# Allow null short_code briefly on insert; Base62(pk) assigned immediately after save.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0003_url_click_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='short_code',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True),
        ),
    ]
