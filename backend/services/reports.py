from collections import Counter
import csv
from datetime import date, datetime, time, timezone
from io import StringIO

from backend.database.supabase import get_supabase_client


PRESCRIPTION_STATUSES = ("Pendente", "Entregue", "Cancelada")
APPOINTMENT_STATUSES = ("Agendada", "Realizada", "Cancelada")
STOCK_MOVEMENT_TYPES = ("Entrada", "Saida")


def get_indicators_report(
    *,
    created_from: date | None = None,
    created_to: date | None = None,
) -> dict:
    patients = _fetch_rows(
        "pacientes",
        "id,created_at",
        created_from=created_from,
        created_to=created_to,
    )
    records = _fetch_rows(
        "medical_records",
        "id,diagnostico,created_at",
        created_from=created_from,
        created_to=created_to,
    )
    prescriptions = _fetch_rows(
        "prescriptions",
        "id,status,created_at",
        created_from=created_from,
        created_to=created_to,
    )
    appointments = _fetch_rows(
        "appointments",
        "id,status,scheduled_at,created_at",
        created_from=created_from,
        created_to=created_to,
        date_column="scheduled_at",
    )
    medications = _fetch_rows("medications", "id,quantidade,estoque_minimo,ativo")
    stock_movements = _fetch_rows(
        "medication_movements",
        "id,tipo,created_at",
        created_from=created_from,
        created_to=created_to,
    )
    users = _fetch_rows("users", "id,ativo")

    prescription_statuses = Counter(item["status"] for item in prescriptions)
    appointment_statuses = Counter(item["status"] for item in appointments)
    stock_movement_types = Counter(item["tipo"] for item in stock_movements)
    low_stock_count = sum(
        1
        for item in medications
        if item.get("ativo")
        and int(item.get("quantidade") or 0) <= int(item.get("estoque_minimo") or 0)
    )
    diagnoses = Counter(
        item["diagnostico"].strip()
        for item in records
        if item.get("diagnostico") and item["diagnostico"].strip()
    )

    return {
        "period": {
            "created_from": created_from.isoformat() if created_from else None,
            "created_to": created_to.isoformat() if created_to else None,
        },
        "totals": {
            "pacientes": len(patients),
            "prontuarios": len(records),
            "prescricoes": len(prescriptions),
            "prescricoes_pendentes": prescription_statuses["Pendente"],
            "consultas": len(appointments),
            "consultas_agendadas": appointment_statuses["Agendada"],
            "consultas_realizadas": appointment_statuses["Realizada"],
            "consultas_canceladas": appointment_statuses["Cancelada"],
            "medicamentos": len(medications),
            "medicamentos_baixo_estoque": low_stock_count,
            "movimentacoes_estoque": len(stock_movements),
            "usuarios_ativos": sum(1 for item in users if item.get("ativo")),
            "usuarios_inativos": sum(1 for item in users if not item.get("ativo")),
        },
        "prescriptions_by_status": [
            {"label": status, "value": prescription_statuses[status]}
            for status in PRESCRIPTION_STATUSES
        ],
        "appointments_by_status": [
            {"label": status, "value": appointment_statuses[status]}
            for status in APPOINTMENT_STATUSES
        ],
        "stock_movements_by_type": [
            {"label": movement_type, "value": stock_movement_types[movement_type]}
            for movement_type in STOCK_MOVEMENT_TYPES
        ],
        "patients_by_month": _bucket_by_month(patients),
        "records_by_day": _bucket_by_day(records),
        "appointments_by_day": _bucket_by_day(appointments, date_field="scheduled_at"),
        "stock_movements_by_day": _bucket_by_day(stock_movements),
        "top_diagnoses": [
            {"label": label, "value": value}
            for label, value in diagnoses.most_common(5)
        ],
    }


def indicators_report_to_csv(report: dict) -> str:
    output = StringIO()
    writer = csv.writer(output, delimiter=";")

    writer.writerow(["Sistema de Prontuarios - Relatorio de Indicadores"])
    writer.writerow(["Periodo inicial", report["period"]["created_from"] or "inicio"])
    writer.writerow(["Periodo final", report["period"]["created_to"] or "hoje"])
    writer.writerow([])

    writer.writerow(["Totais"])
    writer.writerow(["Indicador", "Valor"])
    for key, value in report["totals"].items():
        writer.writerow([_humanize_key(key), value])
    writer.writerow([])

    _write_bucket_section(writer, "Prescricoes por status", report["prescriptions_by_status"])
    _write_bucket_section(writer, "Consultas por status", report["appointments_by_status"])
    _write_bucket_section(writer, "Movimentacoes de estoque por tipo", report["stock_movements_by_type"])
    _write_bucket_section(writer, "Pacientes por mes", report["patients_by_month"])
    _write_bucket_section(writer, "Prontuarios por dia", report["records_by_day"])
    _write_bucket_section(writer, "Consultas por dia", report["appointments_by_day"])
    _write_bucket_section(writer, "Movimentacoes de estoque por dia", report["stock_movements_by_day"])
    _write_bucket_section(writer, "Principais diagnosticos", report["top_diagnoses"])

    return output.getvalue()


def _fetch_rows(
    table: str,
    columns: str,
    *,
    created_from: date | None = None,
    created_to: date | None = None,
    date_column: str = "created_at",
) -> list[dict]:
    query = get_supabase_client().table(table).select(columns)

    if created_from:
        starts_at = datetime.combine(created_from, time.min, tzinfo=timezone.utc)
        query = query.gte(date_column, starts_at.isoformat())
    if created_to:
        ends_at = datetime.combine(created_to, time.max, tzinfo=timezone.utc)
        query = query.lte(date_column, ends_at.isoformat())

    response = query.range(0, 9999).execute()
    return response.data


def _bucket_by_month(items: list[dict]) -> list[dict]:
    buckets = Counter()
    for item in items:
        parsed = _parse_datetime(item.get("created_at"))
        if parsed:
            buckets[parsed.strftime("%Y-%m")] += 1

    return [
        {"label": label, "value": buckets[label]}
        for label in sorted(buckets)
    ]


def _bucket_by_day(items: list[dict], *, date_field: str = "created_at") -> list[dict]:
    buckets = Counter()
    for item in items:
        parsed = _parse_datetime(item.get(date_field))
        if parsed:
            buckets[parsed.date().isoformat()] += 1

    return [
        {"label": label, "value": buckets[label]}
        for label in sorted(buckets)
    ]


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def _write_bucket_section(writer, title: str, buckets: list[dict]) -> None:
    writer.writerow([title])
    writer.writerow(["Item", "Valor"])
    if buckets:
        for bucket in buckets:
            writer.writerow([bucket["label"], bucket["value"]])
    else:
        writer.writerow(["Sem dados", 0])
    writer.writerow([])


def _humanize_key(key: str) -> str:
    labels = {
        "pacientes": "Pacientes",
        "prontuarios": "Prontuarios",
        "prescricoes": "Prescricoes",
        "prescricoes_pendentes": "Prescricoes pendentes",
        "consultas": "Consultas",
        "consultas_agendadas": "Consultas agendadas",
        "consultas_realizadas": "Consultas realizadas",
        "consultas_canceladas": "Consultas canceladas",
        "medicamentos": "Medicamentos",
        "medicamentos_baixo_estoque": "Medicamentos em baixo estoque",
        "movimentacoes_estoque": "Movimentacoes de estoque",
        "usuarios_ativos": "Usuarios ativos",
        "usuarios_inativos": "Usuarios inativos",
    }
    return labels.get(key, key)
