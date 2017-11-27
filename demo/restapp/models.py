# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.decorators import method_decorator


class Profile(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL)
    telephone = models.CharField(u'电话号码', max_length=11)

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.pk})

    @property
    def sex(self):
        return 1
