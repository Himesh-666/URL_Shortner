# Generated manually for click tracking

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0002_url_calls_remaining_url_expires_at_url_password_hash_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='click_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
