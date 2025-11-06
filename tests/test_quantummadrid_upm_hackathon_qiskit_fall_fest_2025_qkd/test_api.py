__copyright__ = 'Copyright (c) 2025 The QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD project authors. All rights reserved.'
__author__ = 'Rafael J. Vicente <rafaelj.vicente@upm.es>'

import unittest

from fastapi import status
from fastapi.testclient import TestClient

from quantummadrid_upm_hackathon_qiskit_fall_fest_2025_qkd.api import app

client = TestClient(app)


class TestBaseEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.base_url = '/api/v1/keys'

    def test_root_redirect(self) -> None:
        response = client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('/docs', response.text)
