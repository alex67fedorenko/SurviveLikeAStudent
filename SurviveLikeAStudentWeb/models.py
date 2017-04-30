# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=255)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_short_text(self):
        if len(self.text) > 100:
            return self.text[:100]
        else:
            return self.text


class Profile(models.Model):
    user = models.ForeignKey('auth.User')
    full_name = models.CharField(max_length=100)
    about = models.TextField(max_length=255)
    score = models.IntegerField(default=0)
    image = models.ImageField(upload_to="static/images")
