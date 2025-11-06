__copyright__ = 'Copyright (c) 2025 The QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD project authors. All rights reserved.'
__author__ = 'Rafael J. Vicente <rafaelj.vicente@upm.es>'

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routers import etsi_gs_qkd_014, qrng

app = FastAPI(title='ETSI GS QKD 014 & QRNG API', version='1.0.0')

app.include_router(etsi_gs_qkd_014.router)
app.include_router(qrng.router)


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def redirect_root() -> str:
    return "/docs"
