__copyright__ = 'Copyright (c) 2025 The QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD project authors. All rights reserved.'
__author__ = 'Rafael J. Vicente <rafaelj.vicente@upm.es>'

import base64
from secrets import token_bytes
from typing import Annotated

from pydantic import Base64Encoder, EncodedBytes, Field


class Base64EncoderNoNL(Base64Encoder):
    @classmethod
    def encode(cls, value: bytes) -> bytes:
        return base64.standard_b64encode(value)  # standard_b64encode function does not add "\n" at the end of the str


Base64BytesNoNL = Annotated[bytes, EncodedBytes(encoder=Base64EncoderNoNL)]

Base64FieldNoNL = Field(
    description='Base64-encoded key material',
    json_schema_extra={'example': base64.b64encode(token_bytes(32)).decode()}
)
