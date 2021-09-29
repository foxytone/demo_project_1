from django.test import TestCase


class TestView(TestCase):
    def test_correct_html_page(self):
        uni_pattern_for_pair_tags = '[^>]*>.*(.|\n)*</'

        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks.html')
        self.assertTemplateUsed(response, 'base.html')

        html = response.content.decode('utf-8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'), 'Начало страницы не с DOCTYPE')
        self.assertIn('<title>Tasks</title>', html, 'Title не "To-Do lists"')
        self.assertRegex(expected_regex=f'<html{uni_pattern_for_pair_tags}html>', text=html,
                         msg="не найден <html> тэг")
        self.assertRegex(expected_regex=f'<body{uni_pattern_for_pair_tags}body>', text=html,
                         msg="Не найден <body>")
        self.assertRegex(expected_regex=f'<h1{uni_pattern_for_pair_tags}h1>', text=html, msg="не найден заголовок")
