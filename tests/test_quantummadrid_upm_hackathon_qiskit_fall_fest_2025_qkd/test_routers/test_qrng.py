__copyright__ = 'Copyright (c) 2025 The QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD project authors. All rights reserved.'
__author__ = 'Alberto Sebastian <aj.sebastian@upm.es>'

import unittest

from fastapi import status
from fastapi.testclient import TestClient

from quantummadrid_upm_hackathon_qiskit_fall_fest_2025_qkd.api import app
from quantummadrid_upm_hackathon_qiskit_fall_fest_2025_qkd.routers.qrng import QrngKeyDTO

client = TestClient(app)


class TestQrngEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.base_url = '/api/v1/qrng'

    def test_get_qrng_invalid_size(self) -> None:
        invalid_key_size = 2
        response = client.get(f'{self.base_url}?size={invalid_key_size}')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_CONTENT)

        not_multiple_of_8_key_size = 127
        response = client.get(f'{self.base_url}?size={not_multiple_of_8_key_size}')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_CONTENT)

    def test_get_qrng_valid_size(self) -> None:
        correct_key_size = 256
        response = client.get(f'{self.base_url}?size={correct_key_size}')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dto = QrngKeyDTO(**response.json())
        self.assertEqual(len(dto.key), correct_key_size / 8)

        correct_key_size = 512
        response = client.get(f'{self.base_url}?size={correct_key_size}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dto = QrngKeyDTO(**response.json())
        self.assertEqual(len(dto.key), correct_key_size / 8)


if __name__ == "__main__":
    unittest.main()
