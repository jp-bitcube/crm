from django.test import TestCase
from django.shortcuts import reverse


class LandingPageTest(TestCase):

    def test_get(self):
        response = self.client.get(reverse("landing_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing_page.html")

    # def test_template_name(self):
    #     response = self.client.get(reverse("landing_page"))
    #     self.assertTemplateUsed(response, "landing_page.html")
