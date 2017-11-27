# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    """代码片段"""

    created = models.DateTimeField(u"创建时间", auto_now_add=True)
    title = models.CharField(u"标题", max_length=100, blank=True, default='')
    code = models.TextField(u"代码")
    linenos = models.BooleanField(u"是否带行号", default=False)
    language = models.CharField(u"语言", choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(u"样式", choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField(u'高亮')

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)
