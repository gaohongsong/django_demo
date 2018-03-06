# -*- coding: utf-8 -*-

from django.test import TestCase
from snippets.models import Snippet


class SnippetTest(TestCase):
    """ Test module for Snippet model """

    def setUp(self):
        Snippet.objects.create(title=u"title1", code=u"代码1", language="python", owner_id=1)
        Snippet.objects.create(title=u"title2", code=u"代码2", language="java", owner_id=2)

    def test_get_language(self):
        snippet = Snippet.objects.get(title='title1')
        self.assertEqual(snippet.get_language(), "python")
