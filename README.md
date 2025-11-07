# 🌌 QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD

[![Hackathon](https://img.shields.io/badge/Event-Hackathon:%20Qiskit%20Fall%20Fest%202025-purple)](https://quantummadrid.github.io/)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)](https://fastapi.tiangolo.com/)
[![Last Commit](https://img.shields.io/github/last-commit/RafaelJVicente/QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD)](https://github.com/RafaelJVicente/QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD/commits/main)
[![Release](https://img.shields.io/github/v/release/RafaelJVicente/QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD)](https://github.com/RafaelJVicente/QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD/releases)
[![Build Status](https://img.shields.io/github/actions/workflow/status/RafaelJVicente/QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD/release.yml?branch=main)](https://github.com/RafaelJVicente/QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD/actions)
[![Code quality and security check](https://img.shields.io/github/actions/workflow/status/RafaelJVicente/QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD/code_quality.yml?branch=main&label=code+quality+and+security+check)](https://github.com/RafaelJVicente/QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD/actions)
---

## 🌐 Idioma / Language

🇪🇸 [Español](#-español) | 🇬🇧 [English](#-english)

---

# 🇪🇸 Español

**Simulador ETSI GS QKD 014 y QRNG** desarrollado para el **Quantum Madrid UPM Hackathon - Qiskit Fall Fest 2025**.  
Implementa un servicio **FastAPI** que expone endpoints para simular la extracción de claves simétricas QKD y una fuente
cuántica de números aleatorios.

---

## ✨ Características del proyecto

| Característica                    | Descripción                                                                  |
|-----------------------------------|------------------------------------------------------------------------------|
| 🔑 **Endpoints QKD**              | `/api/v1/keys/{bob_sae_id}/enc_keys`, `/api/v1/keys/{alice_sae_id}/dec_keys` |
| 🔑 **Endpoints QRNG**             | `/api/v1/qrng`                                                               |
| 🔒 **Compatibilidad HTTPS (TLS)** | Soporte HTTPS y posibilidad de utilizar certificados PEM opcionales          |
| 🐍 **Python 3.9+**                | Probado y optimizado para esta versión                                       |
| 🚀 **FastAPI**                    | API que integra OpenAPI (Swagger UI) para facilitar su aprendizaje y uso     |

---

## 📦 Instalación

### 1. Crear entorno virtual

```bash
python3.9 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

### 2. Instalar directamente desde GitHub

```bash
pip install git+https://github.com/RafaelJVicente/QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD.git
```

> Si usas entornos virtuales, activa el tuyo antes de ejecutar el comando.

### 3. Verificar la instalación

```bash
qstart-https-service --help
```

Si ves el mensaje de ayuda con las opciones del servidor, la instalación fue exitosa ✅

---

## ⚙️ Uso

### 🔹 Servidor HTTP (por defecto)

El comando `qstart-http-service` inicia un servidor HTTP con parámetros configurables.

```bash
qstart-http-service --port 22222
```

> Usa -h o --help para ver la lista de posibles parámetros.

### 🔹 Servidor HTTPS (TLS)

El comando `qstart-https-service` inicia un servidor HTTPS con certificados autofirmados preinstalados:

```bash
qstart-https-service --port 22222
```

---

## 🧭 Interfaz Web (Swagger / OpenAPI)

El servicio está implementado con **FastAPI**, y la ruta raíz (`/`) redirige automáticamente a **`/docs`**, donde se
carga la interfaz **OpenAPI (Swagger UI)** para probar los endpoints REST de forma interactiva.

http://0.0.0.0:22222/ o https://0.0.0.0:22222/

---

## 🔑 Endpoints disponibles

### 1. `/api/v1/qrng`

Simula una **fuente cuántica de números aleatorios (QRNG)**.  
Ejemplo:

```bash
curl -X GET http://0.0.0.0:22222/api/v1/qrng?size=512 -H "Content-Type: application/json" -w '\n'
```

> **size** debe ser múltiplo de 8 (resultados codificados en Base64).

---

### 2. `/api/v1/keys/<bob_sae_id>/enc_keys`

Simula la extracción de una clave de **cifrado** para “BOB”.

```bash
curl -X GET http://0.0.0.0:22222/api/v1/keys/BOB_sae/enc_keys -H "Content-Type: application/json" -w '\n'
```

---

### 3. `/api/v1/keys/<alice_sae_id>/dec_keys`

Simula la extracción de la clave de **descifrado** asociada a un `key_ID`.

```bash
curl -X GET http://0.0.0.0:22222/api/v1/keys/ALICE_sae/dec_keys?key_ID=12345678-1234-1234-1234-123456789ABC -H "Content-Type: application/json" -w '\n'
```

---

## 👥 Autores

- **Rafael J. Vicente** <rafaelj.vicente@upm.es>, Universidad Politécnica de Madrid (UPM)
- **Alberto Sebastian** <aj.sebastian@upm.es>, Universidad Politécnica de Madrid (UPM)

---

Copyright (c) 2025 Los autores del proyecto QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD. Todos los derechos
reservados.


---

# 🇬🇧 English

**ETSI GS QKD 014 and QRNG Simulator** developed for the **Quantum Madrid UPM Hackathon - Qiskit Fall Fest 2025**.  
Implements a **FastAPI** service exposing endpoints that simulate symmetric QKD key extraction and a quantum random
number source.

---

## ✨ Project Features

| Feature                          | Description                                                                  |
|----------------------------------|------------------------------------------------------------------------------|
| 🔑 **QKD Endpoints**             | `/api/v1/keys/{bob_sae_id}/enc_keys`, `/api/v1/keys/{alice_sae_id}/dec_keys` |
| 🔑 **QRNG Endpoints**            | `/api/v1/qrng`                                                               |
| 🔒 **HTTPS (TLS) Compatibility** | HTTPS support and optional PEM certificate usage                             |
| 🐍 **Python 3.9+**               | Tested and optimized for this version                                        |
| 🚀 **FastAPI**                   | API integrates OpenAPI (Swagger UI) for easier learning and testing          |

---

## 📦 Installation

### 1. Create a virtual environment

```bash
python3.9 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

### 2. Install directly from GitHub

```bash
pip install git+https://github.com/RafaelJVicente/QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD.git
```

> If you use virtual environments, make sure yours is activated before running the command.

### 3. Verify installation

```bash
qstart-https-service --help
```

If the help message appears, installation was successful ✅

---

## ⚙️ Usage

### 🔹 HTTP Server (default)

The `qstart-http-service` command starts an HTTP server with configurable parameters.

```bash
qstart-http-service --port 22222
```

> Use -h or --help to see available parameters.

### 🔹 HTTPS Server (TLS)

The `qstart-https-service` command starts an HTTPS server with preinstalled self-signed certificates:

```bash
qstart-https-service --port 22222
```

---

## 🧭 Web Interface (Swagger / OpenAPI)

The service is built with **FastAPI**, and the root path (`/`) automatically redirects to **`/docs`**, where the *
*OpenAPI (Swagger UI)** interface is available to test REST endpoints interactively.

http://0.0.0.0:22222/ or https://0.0.0.0:22222/

---

## 🔑 Available Endpoints

### 1. `/api/v1/qrng`

Simulates a **quantum random number generator (QRNG)**.  
Example:

```bash
curl -X GET http://0.0.0.0:22222/api/v1/qrng?size=512 -H "Content-Type: application/json" -w '\n'
```

> **size** must be a multiple of 8 (results are Base64-encoded).

---

### 2. `/api/v1/keys/<bob_sae_id>/enc_keys`

Simulates **encryption key** extraction for “BOB”.

```bash
curl -X GET http://0.0.0.0:22222/api/v1/keys/BOB_sae/enc_keys -H "Content-Type: application/json" -w '\n'
```

---

### 3. `/api/v1/keys/<alice_sae_id>/dec_keys`

Simulates **decryption key** extraction associated with a given `key_ID`.

```bash
curl -X GET http://0.0.0.0:22222/api/v1/keys/ALICE_sae/dec_keys?key_ID=12345678-1234-1234-1234-123456789ABC -H "Content-Type: application/json" -w '\n'
```

---

## 👥 Authors

- **Rafael J. Vicente** <rafaelj.vicente@upm.es>, Universidad Politécnica de Madrid (UPM)
- **Alberto Sebastian** <aj.sebastian@upm.es>, Universidad Politécnica de Madrid (UPM)

---

Copyright (c) 2025 The QuantumMadrid-UPM-Hackathon-Qiskit-Fall-Fest-2025-QKD project authors. All rights reserved.