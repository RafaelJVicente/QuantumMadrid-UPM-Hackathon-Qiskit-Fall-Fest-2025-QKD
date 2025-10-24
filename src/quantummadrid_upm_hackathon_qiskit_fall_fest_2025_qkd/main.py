"""
Author: Rafael J. Vicente <rafaelj.vicente@upm.es>
"""
import argparse
from typing import Annotated

import uvicorn
from annotated_types import Ge, Le
from pydantic import BaseModel

Port = Annotated[int, Ge(0), Le(65535)]
DEFAULT_PORT = 8000


class Config(BaseModel):
    port: Port = DEFAULT_PORT


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT,
                        help=f'Port to run the API on (default: {DEFAULT_PORT})')
    args = parser.parse_args()
    config = Config(port=args.port)

    uvicorn.run('quantummadrid_upm_hackathon_qiskit_fall_fest_2025_qkd.etsi_gs_qkd_014_api:app',
                host='0.0.0.0', port=config.port, reload=False)


if __name__ == '__main__':
    main()
