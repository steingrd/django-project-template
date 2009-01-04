#!/usr/bin/env python

from django.db import models


class Entry(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __unicode__(self):
        return self.title
