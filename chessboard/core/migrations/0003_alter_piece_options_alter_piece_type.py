# Generated by Django 4.0.3 on 2022-03-06 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_piece_color_alter_piece_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='piece',
            options={
                'ordering': ['color', 'type'],
                'verbose_name': 'Piece',
                'verbose_name_plural': 'Pieces',
            },
        ),
        migrations.AlterField(
            model_name='piece',
            name='type',
            field=models.CharField(
                choices=[
                    ('K', 'King'),
                    ('Q', 'Queen'),
                    ('R', 'Rook'),
                    ('B', 'Bishop'),
                    ('N', 'Knight'),
                    ('P', 'Pawn'),
                ],
                max_length=1,
            ),
        ),
    ]