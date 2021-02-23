from unittest import TestCase
from xml.etree import ElementTree

from app import app, GOOD_BOY_URL


class WhatsappReplyTestCase(TestCase):
    def test_invalid_data(self):
        with app.test_client() as client:
            response = client.get('/whatsapp')

        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid request:', response.data)

    def test_get_without_image(self):
        with app.test_client() as client:
            response = client.get('/whatsapp', data={'NumMedia': '0'})

        self.assertEqual(response.status_code, 200)
        content = ElementTree.fromstring(response.data.decode())
        self.assertEqual(content.find('./Message').text, 'Send us an image!')

    def test_post_without_image(self):
        with app.test_client() as client:
            response = client.post('/whatsapp', data={'NumMedia': '0'})

        self.assertEqual(response.status_code, 200)
        content = ElementTree.fromstring(response.data.decode())
        self.assertEqual(content.find('./Message').text, 'Send us an image!')

    def test_get_with_image(self):
        with app.test_client() as client:
            response = client.get(
                '/whatsapp',
                data={
                    'NumMedia': '1',
                    'MediaUrl0': 'http://fake_image/id',
                    'MediaContentType0': 'image/png',
                },
            )

        self.assertEqual(response.status_code, 200)

        content = ElementTree.fromstring(response.data.decode())
        self.assertEqual(
            content.find('./Message').text, "Thanks for the image. Here's one for you!"
        )
        self.assertEqual(content.find('./Message/Media').text, GOOD_BOY_URL)

    def test_post_with_image(self):
        with app.test_client() as client:
            response = client.post(
                '/whatsapp',
                data={
                    'NumMedia': '1',
                    'MediaUrl0': 'http://fake_image/id',
                    'MediaContentType0': 'image/png',
                },
            )

        self.assertEqual(response.status_code, 200)
        content = ElementTree.fromstring(response.data.decode())
        self.assertEqual(
            content.find('./Message').text, "Thanks for the image. Here's one for you!"
        )
        self.assertEqual(content.find('./Message/Media').text, GOOD_BOY_URL)
