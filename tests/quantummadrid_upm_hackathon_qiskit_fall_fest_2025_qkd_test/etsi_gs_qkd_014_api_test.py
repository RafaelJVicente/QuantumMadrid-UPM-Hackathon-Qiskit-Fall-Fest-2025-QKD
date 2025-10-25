"""
Author: Rafael J. Vicente <rafaelj.vicente@upm.es>
"""
import unittest
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from quantummadrid_upm_hackathon_qiskit_fall_fest_2025_qkd.etsi_gs_qkd_014_api import (
    DEFAULT_QRNG_SAE,
    DEFAULT_QRNG_UUID,
    EtsiGsQkd014ResponseDTO,
    app,
)

client = TestClient(app)


class TestKeyEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.base_url = '/api/v1/keys'

    def test_root_redirect(self) -> None:
        response = client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('/docs', response.text)

    def test_get_enc_keys_qrng_mode(self) -> None:
        response = client.get(f'{self.base_url}/{DEFAULT_QRNG_SAE}/enc_keys')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dto = EtsiGsQkd014ResponseDTO(**response.json())
        self.assertEqual(dto.keys[0].key_ID, DEFAULT_QRNG_UUID)

    def test_get_enc_keys_no_qrng_invalid_size(self) -> None:
        slave_sae_id = 'non_qrng_sae'
        invalid_key_size = 128
        response = client.get(f'{self.base_url}/{slave_sae_id}/enc_keys?size={invalid_key_size}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('For QKD keys, size', response.text)

    def test_get_enc_keys_no_qrng_size(self) -> None:
        slave_sae_id = 'non_qrng_sae'
        correct_key_size = 256
        response = client.get(f'{self.base_url}/{slave_sae_id}/enc_keys?size={correct_key_size}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dto = EtsiGsQkd014ResponseDTO(**response.json())
        self.assertNotEqual(dto.keys[0].key_ID, DEFAULT_QRNG_UUID)
        self.assertEqual(len(dto.keys[0].key), correct_key_size / 8)

    def test_get_enc_keys_qrng_size(self) -> None:
        custom_key_size = 128
        response = client.get(f'{self.base_url}/{DEFAULT_QRNG_SAE}/enc_keys?size={custom_key_size}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dto = EtsiGsQkd014ResponseDTO(**response.json())
        self.assertEqual(dto.keys[0].key_ID, DEFAULT_QRNG_UUID)
        self.assertEqual(len(dto.keys[0].key), custom_key_size / 8)

    def test_get_dec_keys_with_qrng_sae(self) -> None:
        invalid_master_sae_id = DEFAULT_QRNG_SAE
        key_id = uuid4()
        response = client.get(f'{self.base_url}/{invalid_master_sae_id}/dec_keys?key_ID={key_id}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Incorrect SAE', response.text)

    def test_get_dec_keys_with_qrng_uuid(self) -> None:
        master_sae_id = 'master_sae'
        invalid_key_id = DEFAULT_QRNG_UUID
        response = client.get(f'{self.base_url}/{master_sae_id}/dec_keys?key_ID={invalid_key_id}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cannot use QRNG UUID', response.text)

    def test_get_dec_keys_valid(self) -> None:
        master_sae_id = 'master_sae'
        slave_sae_id = 'slave_sae'
        response = client.get(f'{self.base_url}/{slave_sae_id}/enc_keys')
        enc_keys_dto = EtsiGsQkd014ResponseDTO(**response.json())
        key_id = enc_keys_dto.keys[0].key_ID
        response = client.get(f'{self.base_url}/{master_sae_id}/dec_keys?key_ID={key_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dec_keys_dto = EtsiGsQkd014ResponseDTO(**response.json())
        self.assertEqual(enc_keys_dto.keys[0], dec_keys_dto.keys[0])


if __name__ == "__main__":
    unittest.main()
