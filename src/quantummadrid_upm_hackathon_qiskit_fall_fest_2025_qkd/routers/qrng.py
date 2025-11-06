__copyright__ = 'Copyright (c) 2025 The QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD project authors. All rights reserved.'
__author__ = 'Alberto Sebastian <aj.sebastian@upm.es>'

import secrets
from base64 import b64encode
from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import BaseModel

from .utils import Base64BytesNoNL, Base64FieldNoNL

DEFAULT_KEY_SIZE_IN_BYTES = 32
DEFAULT_KEY_SIZE = DEFAULT_KEY_SIZE_IN_BYTES * 8


class QrngKeyDTO(BaseModel):
    key: Base64BytesNoNL = Base64FieldNoNL


def get_qrng_key(n_bytes: int) -> bytes:
    key_bytes = secrets.token_bytes(n_bytes)
    return key_bytes


router = APIRouter()


@router.get('/api/v1/qrng', response_model=QrngKeyDTO)
def get_qrng(
        size: Annotated[
            int,
            Query(
                ge=8,
                multiple_of=8,
                description=f"(Optional) Size of the key in bits, default value is {DEFAULT_KEY_SIZE}",
            ),
        ] = DEFAULT_KEY_SIZE,
) -> QrngKeyDTO:
    key_len = size // 8
    key_bytes = get_qrng_key(key_len)
    return QrngKeyDTO(key=b64encode(key_bytes))
