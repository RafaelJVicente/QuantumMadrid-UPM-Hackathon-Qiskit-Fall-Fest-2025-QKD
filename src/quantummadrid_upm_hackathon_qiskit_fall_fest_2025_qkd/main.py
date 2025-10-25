"""
Author: Rafael J. Vicente <rafaelj.vicente@upm.es>
"""
import argparse
from importlib.resources import files
from typing import Annotated, Optional

import uvicorn
from annotated_types import Ge, Le
from pydantic import BaseModel, FilePath

Port = Annotated[int, Ge(0), Le(65535)]


class Config(BaseModel):
    host: str = '0.0.0.0'
    port: Port = 22222
    cert: Optional[FilePath] = None
    key: Optional[FilePath] = None
    ca_cert: Optional[FilePath] = None


def main(default_cer: Optional[str] = None, default_key: Optional[str] = None) -> None:
    default = Config()
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', type=str, default=default.host,
                        help=f'Server hostname or IP to run the API on (default: {default.host})')
    parser.add_argument('-p', '--port', type=int, default=default.port,
                        help=f'Server port to run the API on (default: {default.port})')
    parser.add_argument('--cert', type=str, default=default.cert,
                        help=f'Path to server certificate file in PEM format (default: {default.cert})')
    parser.add_argument('--key', type=str, default=default.key,
                        help=f'Path to server private key file in PEM format (default: {default.key})')
    parser.add_argument('--cacert', type=str, default=default.ca_cert,
                        help=f'Path to clients CA certificate file  in PEM format (default: {default.ca_cert})')

    args = parser.parse_args()
    cert = args.cert or default_cer or default.cert
    key = args.key or default_key or default.key

    if (cert and not key) or (key and not cert):
        parser.error("You must specify both --cert and --key together.")

    config = Config(host=args.host, port=args.port, cert=args.cert, key=args.key, ca_cert=args.cacert)

    uvicorn.run('quantummadrid_upm_hackathon_qiskit_fall_fest_2025_qkd.etsi_gs_qkd_014_api:app',
                host=config.host, port=config.port, reload=False,
                ssl_certfile=cert, ssl_keyfile=key, ssl_ca_certs=config.ca_cert)


def tls_main() -> None:
    tls_path = files('quantummadrid_upm_hackathon_qiskit_fall_fest_2025_qkd').joinpath('tls')
    cert, key = map(str, map(tls_path.joinpath, ('server.crt', 'server.key')))
    main(str(cert), str(key))


if __name__ == '__main__':
    main()
