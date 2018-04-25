# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-27 06:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

try:
    from typing import List,Any
except ImportError:
    print("WARNING: Typing module is not find")

class Migration(migrations.Migration):

    initial = True  # type: bool

    dependencies = [
    ]  # type: List[object]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=200)),
                ('correct', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=50)),
                ('topic', models.CharField(max_length=50)),
                ('points', models.IntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_questions', models.IntegerField(default=10)),
                ('min_pass', models.IntegerField(default=10)),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Quiz'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Question'),
        ),
    ]  # type: List[Any]
