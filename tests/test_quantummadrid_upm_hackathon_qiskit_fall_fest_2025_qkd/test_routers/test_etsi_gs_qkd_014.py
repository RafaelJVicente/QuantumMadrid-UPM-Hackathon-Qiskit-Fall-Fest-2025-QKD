__copyright__ = 'Copyright (c) 2025 The QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD project authors. All rights reserved.'
__author__ = 'Rafael J. Vicente <rafaelj.vicente@upm.es>'

import unittest

from fastapi import status
from fastapi.testclient import TestClient

from quantummadrid_upm_hackathon_qiskit_fall_fest_2025_qkd.api import app
from quantummadrid_upm_hackathon_qiskit_fall_fest_2025_qkd.routers.etsi_gs_qkd_014 import EtsiGsQkd014ResponseDTO

client = TestClient(app)


class TestEtsiQkd014Endpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.base_url = '/api/v1/keys'

    def test_get_enc_keys_invalid_size(self) -> None:
        bob_sae_id = 'bob_sae'
        invalid_key_size = 128
        response = client.get(f'{self.base_url}/{bob_sae_id}/enc_keys?size={invalid_key_size}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('For QKD keys, size', response.text)

    def test_get_enc_keys_valid_size(self) -> None:
        bob_sae_id = 'bob_sae'
        correct_key_size = 256
        response = client.get(f'{self.base_url}/{bob_sae_id}/enc_keys?size={correct_key_size}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dto = EtsiGsQkd014ResponseDTO(**response.json())
        self.assertEqual(len(dto.keys[0].key), correct_key_size / 8)

    def test_get_dec_keys_valid(self) -> None:
        alice_sae_id = 'alice_sae'
        bob_sae_id = 'bob_sae'
        response = client.get(f'{self.base_url}/{bob_sae_id}/enc_keys')
        enc_keys_dto = EtsiGsQkd014ResponseDTO(**response.json())
        key_id = enc_keys_dto.keys[0].key_ID
        response = client.get(f'{self.base_url}/{alice_sae_id}/dec_keys?key_ID={key_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dec_keys_dto = EtsiGsQkd014ResponseDTO(**response.json())
        self.assertEqual(enc_keys_dto.keys[0], dec_keys_dto.keys[0])


if __name__ == "__main__":
    unittest.main()
