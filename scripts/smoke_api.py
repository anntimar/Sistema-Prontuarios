import json
import os
from urllib import parse, request


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")
EMAIL = os.getenv("SMOKE_EMAIL", "medico@hospital.com")
PASSWORD = os.getenv("SMOKE_PASSWORD", "Medico@123")


def call(path, *, method="GET", token=None, data=None, form=None):
    headers = {}
    body = None

    if token:
        headers["Authorization"] = f"Bearer {token}"
    if form is not None:
        body = parse.urlencode(form).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = request.Request(
        f"{API_URL}{path}",
        data=body,
        headers=headers,
        method=method,
    )
    with request.urlopen(req, timeout=10) as response:
        raw = response.read().decode("utf-8")
        return response.status, json.loads(raw) if raw else None


def main():
    health_status, health = call("/health")
    print(f"health: {health_status} {health}")

    login_status, login = call(
        "/login",
        method="POST",
        form={"email": EMAIL, "senha": PASSWORD},
    )
    print(f"login: {login_status} {EMAIL}")
    token = login["access_token"]

    patients_status, patients = call("/pacientes", token=token)
    print(f"pacientes: {patients_status} {len(patients['items'])} item(ns)")

    records_status, records = call("/prontuarios", token=token)
    print(f"prontuarios: {records_status} {len(records['items'])} item(ns)")

    prescriptions_status, prescriptions = call("/prescricoes", token=token)
    print(f"prescricoes: {prescriptions_status} {len(prescriptions['items'])} item(ns)")

    attachments_status, attachments = call("/anexos", token=token)
    print(f"anexos: {attachments_status} {len(attachments['items'])} item(ns)")


if __name__ == "__main__":
    main()
