"""
Author: Rafael J. Vicente <rafaelj.vicente@upm.es>
"""
import base64
import logging
import secrets
from random import Random
from typing import Annotated, List, Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Path, Query, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import Base64Encoder, BaseModel, EncodedBytes, StringConstraints

DEFAULT_QRNG_UUID = UUID('00000000-0000-0000-0000-000000000000')
DEFAULT_QRNG_SAE = 'qrng'

DEFAULT_KEY_SIZE_IN_BYTES = 32
DEFAULT_KEY_SIZE = DEFAULT_KEY_SIZE_IN_BYTES * 8
SAE = Annotated[str, StringConstraints(pattern=r'^[a-zA-Z0-9._-]+$')]


class Base64EncoderNoNL(Base64Encoder):
    @classmethod
    def encode(cls, value: bytes) -> bytes:
        return base64.standard_b64encode(value)  # standard_b64encode function does not add "\n" at the end of the str


Base64BytesNoNL = Annotated[bytes, EncodedBytes(encoder=Base64EncoderNoNL)]


class EtsiGsQkd014KeyDTO(BaseModel):
    key_ID: UUID
    key: Base64BytesNoNL


class EtsiGsQkd014ResponseDTO(BaseModel):
    keys: List[EtsiGsQkd014KeyDTO]


def is_qrng_uuid(uuid_str: UUID) -> bool:
    return uuid_str == DEFAULT_QRNG_UUID


def generate_random_key_id() -> UUID:
    while is_qrng_uuid(key_id := uuid4()):
        pass
    return key_id


def get_pseudo_random_key(n_bytes: int, key_id: Optional[UUID] = None) -> EtsiGsQkd014KeyDTO:
    if key_id is None:
        key_id = generate_random_key_id()
    seed = key_id.int
    key_bytes = Random(seed).randbytes(n_bytes)
    return EtsiGsQkd014KeyDTO(key_ID=key_id, key=base64.b64encode(key_bytes))


def get_full_random_key(n_bytes: int) -> EtsiGsQkd014KeyDTO:
    key_bytes = secrets.token_bytes(n_bytes)
    return EtsiGsQkd014KeyDTO(key_ID=DEFAULT_QRNG_UUID, key=base64.b64encode(key_bytes))


app = FastAPI(title='ETSI GS QKD 014 QRNG API', version='1.1.1')


@app.exception_handler(RuntimeError)
async def unicorn_exception_handler(request: Request, exc: RuntimeError) -> JSONResponse:
    logging.error(f'Uncaught exception: {str(exc).strip()}')
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={'message': 'Error on server side.', 'detail': str(exc)},
    )


@app.get("/", response_class=RedirectResponse)
async def redirect_root() -> str:
    return "/docs"


@app.get('/api/v1/keys/{slave_sae_id}/enc_keys', response_model=EtsiGsQkd014ResponseDTO)
def get_enc_keys(
        slave_sae_id: Annotated[SAE, Path(description="SAE ID")],
        number: Annotated[
            int, Query(ge=1, description="(Optional) Number of keys requested, default value is 1.")
        ] = 1,
        size: Annotated[
            int,
            Query(
                ge=8,
                multiple_of=8,
                description="(Optional) Size of each key in bits, default value is defined as"
                            " key_size in Status data format.",
            ),
        ] = DEFAULT_KEY_SIZE,
) -> EtsiGsQkd014ResponseDTO:
    using_qrng_mode = slave_sae_id.lower() == DEFAULT_QRNG_SAE
    if not using_qrng_mode and size != DEFAULT_KEY_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'For QKD keys, size {size} is fixed to {DEFAULT_KEY_SIZE}.'
        )

    key_len = size // 8
    enc_keys = []

    for _ in range(number):
        key = get_full_random_key(key_len) if using_qrng_mode else get_pseudo_random_key(key_len)
        enc_keys.append(key)
        logging.info(f'Generated key {key}')

    return EtsiGsQkd014ResponseDTO(keys=enc_keys)


@app.get('/api/v1/keys/{master_sae_id}/dec_keys', response_model=EtsiGsQkd014ResponseDTO)
def get_dec_keys(
        master_sae_id: Annotated[SAE, Path(description="SAE ID")],
        key_ID: Annotated[UUID, Query(description="UUID of the key to be retrieved.")],
) -> EtsiGsQkd014ResponseDTO:
    if master_sae_id.lower() == DEFAULT_QRNG_SAE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Incorrect SAE "{master_sae_id}", cannot use {DEFAULT_QRNG_SAE} for dec_keys.'
        )
    if is_qrng_uuid(key_ID):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Cannot use QRNG UUID "{key_ID}" for dec_keys as is a non-qkd key generated in a single source.'
        )

    key_len = DEFAULT_KEY_SIZE // 8

    dec_keys = []
    key = get_pseudo_random_key(key_len, key_ID)
    dec_keys.append(key)
    logging.info(f'Extracted key: {key}')

    return EtsiGsQkd014ResponseDTO(keys=dec_keys)
