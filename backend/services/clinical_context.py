from backend.database.supabase import get_supabase_client


def enrich_medical_records(records: list[dict]) -> list[dict]:
    if not records:
        return records

    patient_names = _fetch_patient_names({item["id_paciente"] for item in records})
    doctor_names = _fetch_user_names({item["id_medico"] for item in records})
    appointment_map = _fetch_appointment_map(
        {
            item["id_consulta"]
            for item in records
            if item.get("id_consulta")
        }
    )

    return [
        {
            **item,
            "paciente_nome": patient_names.get(item["id_paciente"]),
            "medico_nome": doctor_names.get(item["id_medico"]),
            "consulta_status": appointment_map.get(item.get("id_consulta"), {}).get("status"),
            "consulta_scheduled_at": appointment_map.get(item.get("id_consulta"), {}).get("scheduled_at"),
        }
        for item in records
    ]


def enrich_prescriptions(prescriptions: list[dict]) -> list[dict]:
    if not prescriptions:
        return prescriptions

    record_ids = {item["id_prontuario"] for item in prescriptions}
    record_map = _fetch_record_map(record_ids)
    patient_names = _fetch_patient_names(
        {
            record["id_paciente"]
            for record in record_map.values()
            if record.get("id_paciente")
        }
    )
    doctor_names = _fetch_user_names(
        {
            record["id_medico"]
            for record in record_map.values()
            if record.get("id_medico")
        }
    )
    prescription_items = _fetch_prescription_items({item["id"] for item in prescriptions})

    enriched = []
    for item in prescriptions:
        record = record_map.get(item["id_prontuario"])
        if not record:
            enriched.append(item)
            continue

        enriched.append(
            {
                **item,
                "id_paciente": record["id_paciente"],
                "id_medico": record["id_medico"],
                "paciente_nome": patient_names.get(record["id_paciente"]),
                "medico_nome": doctor_names.get(record["id_medico"]),
                "diagnostico": record.get("diagnostico"),
                "prontuario_created_at": record.get("created_at"),
                "itens": prescription_items.get(item["id"], []),
            }
        )

    return enriched


def enrich_appointments(appointments: list[dict]) -> list[dict]:
    if not appointments:
        return appointments

    patient_names = _fetch_patient_names({item["id_paciente"] for item in appointments})
    doctor_names = _fetch_user_names({item["id_medico"] for item in appointments})

    return [
        {
            **item,
            "paciente_nome": patient_names.get(item["id_paciente"]),
            "medico_nome": doctor_names.get(item["id_medico"]),
        }
        for item in appointments
    ]


def _fetch_patient_names(ids: set[str]) -> dict[str, str]:
    if not ids:
        return {}

    response = (
        get_supabase_client()
        .table("pacientes")
        .select("id,nome")
        .in_("id", list(ids))
        .execute()
    )
    return {item["id"]: item["nome"] for item in response.data}


def _fetch_user_names(ids: set[str]) -> dict[str, str]:
    if not ids:
        return {}

    response = (
        get_supabase_client()
        .table("users")
        .select("id,nome,email")
        .in_("id", list(ids))
        .execute()
    )
    return {
        item["id"]: item.get("nome") or item["email"]
        for item in response.data
    }


def _fetch_record_map(ids: set[str]) -> dict[str, dict]:
    if not ids:
        return {}

    response = (
        get_supabase_client()
        .table("medical_records")
        .select("id,id_paciente,id_medico,id_consulta,diagnostico,created_at")
        .in_("id", list(ids))
        .execute()
    )
    return {item["id"]: item for item in response.data}


def _fetch_appointment_map(ids: set[str]) -> dict[str, dict]:
    if not ids:
        return {}

    response = (
        get_supabase_client()
        .table("appointments")
        .select("id,status,scheduled_at")
        .in_("id", list(ids))
        .execute()
    )
    return {item["id"]: item for item in response.data}


def _fetch_prescription_items(ids: set[str]) -> dict[str, list[dict]]:
    if not ids:
        return {}

    response = (
        get_supabase_client()
        .table("prescription_items")
        .select("id,id_prescricao,id_medicamento,quantidade,posologia,created_at")
        .in_("id_prescricao", list(ids))
        .execute()
    )
    items = response.data
    medications = _fetch_medication_map({item["id_medicamento"] for item in items})
    grouped: dict[str, list[dict]] = {}
    for item in items:
        medication = medications.get(item["id_medicamento"], {})
        grouped.setdefault(item["id_prescricao"], []).append(
            {
                **item,
                "medicamento_nome": medication.get("nome"),
                "medicamento_apresentacao": medication.get("apresentacao"),
            }
        )
    return grouped


def _fetch_medication_map(ids: set[str]) -> dict[str, dict]:
    if not ids:
        return {}

    response = (
        get_supabase_client()
        .table("medications")
        .select("id,nome,apresentacao")
        .in_("id", list(ids))
        .execute()
    )
    return {item["id"]: item for item in response.data}
