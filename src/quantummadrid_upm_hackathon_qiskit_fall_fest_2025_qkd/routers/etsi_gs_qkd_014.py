__copyright__ = 'Copyright (c) 2025 The QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD project authors. All rights reserved.'
__author__ = 'Rafael J. Vicente <rafaelj.vicente@upm.es>'

import base64
import logging
from random import Random
from typing import Annotated, List, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Path, Query, status
from pydantic import BaseModel, StringConstraints

from .utils import Base64BytesNoNL, Base64FieldNoNL

DEFAULT_KEY_SIZE_IN_BYTES = 32
DEFAULT_KEY_SIZE = DEFAULT_KEY_SIZE_IN_BYTES * 8
SAE = Annotated[str, StringConstraints(pattern=r'^[a-zA-Z0-9._-]+$')]


class EtsiGsQkd014KeyDTO(BaseModel):
    key_ID: UUID
    key: Base64BytesNoNL = Base64FieldNoNL


class EtsiGsQkd014ResponseDTO(BaseModel):
    keys: List[EtsiGsQkd014KeyDTO]


def get_pseudo_random_key(n_bytes: int, key_id: Optional[UUID] = None) -> EtsiGsQkd014KeyDTO:
    if key_id is None:
        key_id = uuid4()
    seed = key_id.int
    key_bytes = Random(seed).randbytes(n_bytes)
    return EtsiGsQkd014KeyDTO(key_ID=key_id, key=base64.b64encode(key_bytes))


router = APIRouter()


@router.get('/api/v1/keys/{bob_sae_id}/enc_keys', response_model=EtsiGsQkd014ResponseDTO)
def get_enc_keys(
        bob_sae_id: Annotated[SAE, Path(description="SAE ID")],
        number: Annotated[
            int, Query(ge=1, description='(Optional) Number of keys requested, default value is 1.')
        ] = 1,
        size: Annotated[
            int,
            Query(
                ge=8,
                multiple_of=8,
                description=f'(Optional) Size of each key in bits, default value is {DEFAULT_KEY_SIZE}',
            ),
        ] = DEFAULT_KEY_SIZE,
) -> EtsiGsQkd014ResponseDTO:
    logging.info(f'Distributing quantum keys with the peer: {bob_sae_id}')

    if size != DEFAULT_KEY_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'For QKD keys, size {size} is fixed to {DEFAULT_KEY_SIZE}.'
        )

    key_len = size // 8
    enc_keys = []

    for _ in range(number):
        key = get_pseudo_random_key(key_len)
        enc_keys.append(key)
        logging.info(f'Generated QKD key {key}')

    return EtsiGsQkd014ResponseDTO(keys=enc_keys)


@router.get('/api/v1/keys/{alice_sae_id}/dec_keys', response_model=EtsiGsQkd014ResponseDTO)
def get_dec_keys(
        alice_sae_id: Annotated[SAE, Path(description="SAE ID")],
        key_ID: Annotated[UUID, Query(description="UUID of the key to be retrieved.")],
) -> EtsiGsQkd014ResponseDTO:
    logging.info(f'Obtaining quantum key distributed with the peer: {alice_sae_id}')

    key_len = DEFAULT_KEY_SIZE // 8

    dec_keys = []
    key = get_pseudo_random_key(key_len, key_ID)
    dec_keys.append(key)
    logging.info(f'Distilled QKD key: {key}')

    return EtsiGsQkd014ResponseDTO(keys=dec_keys)
