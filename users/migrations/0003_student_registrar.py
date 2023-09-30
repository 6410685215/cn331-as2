# Generated by Django 4.2.5 on 2023-09-29 16:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_remove_course_course_doc'),
        ('users', '0002_rename_name_student_fname_student_lname'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='registrar',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='course.course'),
            preserve_default=False,
        ),
    ]