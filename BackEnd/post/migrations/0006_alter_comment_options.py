# Generated by Django 5.0.1 on 2024-02-10 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_post_comment_count_comment_post_comments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_at']},
        ),
    ]
