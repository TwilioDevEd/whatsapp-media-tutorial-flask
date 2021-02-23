from unittest import TestCase
from unittest.mock import patch, Mock, mock_open
from xml.etree import ElementTree

from app import app


class WhatsappReplyTestCase(TestCase):
    def _patch_requests(self):
        requests_patcher = patch('app.requests.get')
        self._mock_request = requests_patcher.start()
        self._mock_request.return_value = Mock(content=b'')
        self.addCleanup(requests_patcher.stop)

    def _patch_open(self):
        open_patcher = patch('app.open', mock_open())
        self._mock_open = open_patcher.start()
        self.addCleanup(open_patcher.stop)

    def test_invalid_data(self):
        with app.test_client() as client:
            response = client.get('/whatsapp')

        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid request', response.data)

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
        self._patch_requests()
        self._patch_open()

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
        self._mock_request.assert_called_once_with('http://fake_image/id')
        self._mock_open.assert_called_once_with('app_data/id.png', 'wb')
        handle = self._mock_open()
        handle.write.assert_called_once_with(b'')

    def test_post_with_image(self):
        self._patch_requests()
        self._patch_open()

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
        self._mock_request.assert_called_once_with('http://fake_image/id')
        self._mock_open.assert_called_once_with('app_data/id.png', 'wb')
        handle = self._mock_open()
        handle.write.assert_called_once_with(b'')
