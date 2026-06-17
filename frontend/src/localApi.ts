import { ApiError } from "./apiError";
import type {
  AppUser,
  Appointment,
  AppointmentStatus,
  AttachmentType,
  AuditLog,
  ClinicalAttachment,
  CurrentUser,
  IndicatorsReport,
  MedicalRecord,
  Medication,
  PaginatedResponse,
  Patient,
  Prescription,
  PrescriptionItem,
  StockMovement,
  UserRole,
} from "./types";

type LocalUser = AppUser & {
  senha: string;
};

type LocalDb = {
  users: LocalUser[];
  patients: Patient[];
  records: MedicalRecord[];
  prescriptions: Prescription[];
  prescriptionItems: PrescriptionItem[];
  medications: Medication[];
  stockMovements: StockMovement[];
  appointments: Appointment[];
  attachments: ClinicalAttachment[];
  auditLogs: AuditLog[];
};

type LocalRequestOptions = {
  token?: string;
  body?: unknown;
  form?: FormData;
  method?: "GET" | "POST" | "PATCH" | "DELETE";
};

type TokenPayload = {
  id: string;
  email: string;
  role: UserRole;
};

const STORAGE_KEY = "sistema-prontuarios-demo-db-v2";
const TOKEN_PREFIX = "demo-token:";

const seedDb: LocalDb = {
  users: [
    {
      id: "00000000-0000-0000-0000-000000000010",
      email: "admin@hospital.com",
      senha: "Admin@123",
      role: "admin",
      nome: "Administrador Padrao",
      ativo: true,
      created_at: "2026-06-16T00:00:00.000Z",
      updated_at: "2026-06-16T00:00:00.000Z",
    },
    {
      id: "00000000-0000-0000-0000-000000000001",
      email: "medico@hospital.com",
      senha: "Medico@123",
      role: "medico",
      nome: "Medico Padrao",
      ativo: true,
      created_at: "2026-06-16T00:00:00.000Z",
      updated_at: "2026-06-16T00:00:00.000Z",
    },
    {
      id: "00000000-0000-0000-0000-000000000002",
      email: "farmacia@hospital.com",
      senha: "Farmacia@123",
      role: "farmaceutico",
      nome: "Farmacia Padrao",
      ativo: true,
      created_at: "2026-06-16T00:00:00.000Z",
      updated_at: "2026-06-16T00:00:00.000Z",
    },
    {
      id: "00000000-0000-0000-0000-000000000003",
      email: "recepcao@hospital.com",
      senha: "Recepcao@123",
      role: "recepcao",
      nome: "Recepcao Padrao",
      ativo: true,
      created_at: "2026-06-16T00:00:00.000Z",
      updated_at: "2026-06-16T00:00:00.000Z",
    },
  ],
  patients: [
    {
      id: "10000000-0000-0000-0000-000000000001",
      nome: "Joao da Silva",
      cpf: "12345678900",
      data_nascimento: "1990-05-15",
      telefone: "82999999999",
      created_at: "2026-06-16T00:00:00.000Z",
    },
    {
      id: "10000000-0000-0000-0000-000000000002",
      nome: "Maria Oliveira",
      cpf: "09876543211",
      data_nascimento: "1985-10-22",
      telefone: "82988888888",
      created_at: "2026-06-16T00:00:00.000Z",
    },
  ],
  appointments: [
    {
      id: "40000000-0000-0000-0000-000000000001",
      id_paciente: "10000000-0000-0000-0000-000000000001",
      id_medico: "00000000-0000-0000-0000-000000000001",
      scheduled_at: "2026-06-15T14:00:00.000Z",
      status: "Realizada",
      observacoes: "Consulta inicial de acompanhamento.",
      created_at: "2026-06-16T00:00:00.000Z",
      updated_at: "2026-06-16T00:00:00.000Z",
    },
    {
      id: "40000000-0000-0000-0000-000000000002",
      id_paciente: "10000000-0000-0000-0000-000000000002",
      id_medico: "00000000-0000-0000-0000-000000000001",
      scheduled_at: "2026-06-17T14:00:00.000Z",
      status: "Agendada",
      observacoes: "Retorno ambulatorial.",
      created_at: "2026-06-16T00:00:00.000Z",
      updated_at: "2026-06-16T00:00:00.000Z",
    },
  ],
  records: [
    {
      id: "20000000-0000-0000-0000-000000000001",
      id_paciente: "10000000-0000-0000-0000-000000000001",
      id_medico: "00000000-0000-0000-0000-000000000001",
      id_consulta: "40000000-0000-0000-0000-000000000001",
      anamnese: "Paciente relata dor de cabeca recorrente ha tres dias.",
      diagnostico: "Cefaleia tensional",
      observacoes: "Orientado repouso, hidratacao e retorno em caso de piora.",
      created_at: "2026-06-16T00:00:00.000Z",
    },
  ],
  prescriptions: [
    {
      id: "30000000-0000-0000-0000-000000000001",
      id_prontuario: "20000000-0000-0000-0000-000000000001",
      medicamentos: ["Dipirona 500mg a cada 6 horas se dor"],
      status: "Pendente",
      created_at: "2026-06-16T00:00:00.000Z",
      dispensed_at: undefined,
    },
  ],
  prescriptionItems: [
    {
      id: "70000000-0000-0000-0000-000000000001",
      id_prescricao: "30000000-0000-0000-0000-000000000001",
      id_medicamento: "60000000-0000-0000-0000-000000000001",
      quantidade: 1,
      posologia: "Tomar 1 comprimido a cada 6 horas se dor.",
      created_at: "2026-06-16T00:00:00.000Z",
    },
  ],
  medications: [
    {
      id: "60000000-0000-0000-0000-000000000001",
      nome: "Dipirona",
      apresentacao: "500mg",
      quantidade: 120,
      estoque_minimo: 20,
      ativo: true,
      baixo_estoque: false,
      created_at: "2026-06-16T00:00:00.000Z",
      updated_at: "2026-06-16T00:00:00.000Z",
    },
    {
      id: "60000000-0000-0000-0000-000000000002",
      nome: "Ibuprofeno",
      apresentacao: "400mg",
      quantidade: 12,
      estoque_minimo: 15,
      ativo: true,
      baixo_estoque: true,
      created_at: "2026-06-16T00:00:00.000Z",
      updated_at: "2026-06-16T00:00:00.000Z",
    },
    {
      id: "60000000-0000-0000-0000-000000000003",
      nome: "Amoxicilina",
      apresentacao: "500mg",
      quantidade: 40,
      estoque_minimo: 10,
      ativo: true,
      baixo_estoque: false,
      created_at: "2026-06-16T00:00:00.000Z",
      updated_at: "2026-06-16T00:00:00.000Z",
    },
  ],
  stockMovements: [],
  attachments: [
    {
      id: "50000000-0000-0000-0000-000000000001",
      id_paciente: "10000000-0000-0000-0000-000000000001",
      id_prontuario: "20000000-0000-0000-0000-000000000001",
      tipo: "Exame",
      titulo: "Hemograma de exemplo",
      arquivo_url: "https://example.com/exames/hemograma-exemplo.pdf",
      observacoes: "Arquivo demonstrativo para validar o fluxo de anexos clinicos.",
      uploaded_by: "00000000-0000-0000-0000-000000000001",
      uploaded_by_email: "medico@hospital.com",
      created_at: "2026-06-16T00:00:00.000Z",
      updated_at: "2026-06-16T00:00:00.000Z",
    },
  ],
  auditLogs: [],
};

export const isStandaloneMode = import.meta.env.VITE_STANDALONE === "true";

export function getStandaloneApiLabel() {
  return "Demo local no navegador";
}

export async function localApiRequest<T>(
  path: string,
  { token, body, form, method = "GET" }: LocalRequestOptions = {},
): Promise<T> {
  const db = loadDb();
  const url = new URL(path, "http://local");
  const segments = url.pathname.split("/").filter(Boolean);

  if (url.pathname === "/login" && method === "POST") {
    const email = String(form?.get("email") ?? "").trim().toLowerCase();
    const senha = String(form?.get("senha") ?? "");
    const user = db.users.find((item) => item.email === email);
    if (!user || !user.ativo || user.senha !== senha) {
      throw new ApiError("Credenciais invalidas.", 400);
    }
    return { access_token: encodeToken(user) } as T;
  }

  const currentUser = currentUserFromToken(db, token);

  if (url.pathname === "/me") {
    return publicCurrentUser(currentUser) as T;
  }

  if (url.pathname === "/demo/reset" && method === "POST") {
    requireRole(currentUser, "admin");
    saveDb(clone(seedDb));
    return { message: "Base de demonstracao restaurada." } as T;
  }

  if (segments[0] === "pacientes") {
    return handlePatients<T>(db, segments, url, method, body, currentUser);
  }
  if (segments[0] === "prontuarios") {
    return handleRecords<T>(db, segments, url, method, body, currentUser);
  }
  if (segments[0] === "prescricoes") {
    return handlePrescriptions<T>(db, segments, url, method, body, currentUser);
  }
  if (segments[0] === "medicamentos") {
    return handleMedications<T>(db, segments, url, method, body, currentUser);
  }
  if (segments[0] === "consultas") {
    return handleAppointments<T>(db, segments, url, method, body, currentUser);
  }
  if (segments[0] === "anexos") {
    return handleAttachments<T>(db, segments, url, method, body, form, currentUser);
  }
  if (segments[0] === "usuarios") {
    return handleUsers<T>(db, segments, url, method, body, currentUser);
  }
  if (segments[0] === "relatorios" && segments[1] === "indicadores") {
    requireRole(currentUser, "admin");
    return buildReport(db, url) as T;
  }
  if (segments[0] === "auditoria") {
    requireRole(currentUser, "admin");
    return paginate(filterAudit(db.auditLogs, url), url) as T;
  }

  throw new ApiError("Rota local nao implementada.", 404);
}

export async function localApiDownload(
  path: string,
  { token }: { token?: string } = {},
): Promise<Blob> {
  const db = loadDb();
  const user = currentUserFromToken(db, token);
  const url = new URL(path, "http://local");
  if (url.pathname !== "/relatorios/indicadores/export.csv") {
    throw new ApiError("Download local nao implementado.", 404);
  }
  requireRole(user, "admin");
  const report = buildReport(db, url);
  return new Blob([reportToCsv(report)], { type: "text/csv;charset=utf-8" });
}

function handlePatients<T>(
  db: LocalDb,
  segments: string[],
  url: URL,
  method: string,
  body: unknown,
  user: LocalUser,
): T {
  requireAnyRole(user, "admin", "medico", "recepcao");
  if (segments.length === 1 && method === "GET") {
    let items = [...db.patients];
    const search = url.searchParams.get("search");
    const cpf = url.searchParams.get("cpf");
    if (search) {
      items = items.filter((item) => item.nome.toLowerCase().includes(search.toLowerCase()));
    }
    if (cpf) {
      items = items.filter((item) => item.cpf === onlyDigits(cpf));
    }
    return paginate(items, url) as T;
  }
  if (segments.length === 1 && method === "POST") {
    requireAnyRole(user, "admin", "recepcao");
    const data = body as Partial<Patient>;
    const created = {
      id: newId(),
      nome: String(data.nome ?? ""),
      cpf: onlyDigits(String(data.cpf ?? "")),
      data_nascimento: String(data.data_nascimento ?? ""),
      telefone: String(data.telefone ?? ""),
      created_at: now(),
    };
    db.patients.push(created);
    audit(db, user, "patient.create", "patient", created.id, { nome: created.nome });
    saveDb(db);
    return created as T;
  }
  const id = segments[1];
  const patient = db.patients.find((item) => item.id === id);
  if (!patient) {
    throw new ApiError("Paciente nao encontrado.", 404);
  }
  if (method === "PATCH") {
    requireAnyRole(user, "admin", "recepcao");
    Object.assign(patient, body as Partial<Patient>, { cpf: onlyDigits(String((body as Partial<Patient>).cpf ?? patient.cpf)) });
    audit(db, user, "patient.update", "patient", patient.id, { nome: patient.nome });
    saveDb(db);
    return patient as T;
  }
  if (method === "DELETE") {
    requireRole(user, "admin");
    db.patients = db.patients.filter((item) => item.id !== id);
    audit(db, user, "patient.delete", "patient", id);
    saveDb(db);
    return { message: "Paciente removido." } as T;
  }
  return enrichPatient(patient) as T;
}

function handleRecords<T>(
  db: LocalDb,
  segments: string[],
  url: URL,
  method: string,
  body: unknown,
  user: LocalUser,
): T {
  requireAnyRole(user, "admin", "medico", "recepcao");
  if (segments.length === 1 && method === "GET") {
    let items = db.records;
    if (user.role === "medico") {
      items = items.filter((item) => item.id_medico === user.id);
    }
    items = filterByParam(items, url, "id_paciente");
    items = filterByDate(items, url, "created_at", "created_from", "created_to");
    return paginate(enrichRecords(db, items).sort(descBy("created_at")), url) as T;
  }
  if (segments.length === 1 && method === "POST") {
    requireRole(user, "medico");
    const data = body as Partial<MedicalRecord>;
    const appointment = data.id_consulta ? db.appointments.find((item) => item.id === data.id_consulta) : null;
    if (appointment && appointment.status !== "Realizada") {
      throw new ApiError("Apenas consultas realizadas podem gerar prontuario.", 400);
    }
    const created: MedicalRecord = {
      id: newId(),
      id_paciente: String(data.id_paciente ?? ""),
      id_medico: user.id,
      id_consulta: data.id_consulta || undefined,
      anamnese: String(data.anamnese ?? ""),
      diagnostico: String(data.diagnostico ?? ""),
      observacoes: String(data.observacoes ?? ""),
      created_at: now(),
    };
    db.records.push(created);
    audit(db, user, "medical_record.create", "medical_record", created.id);
    saveDb(db);
    return enrichRecords(db, [created]) as T;
  }
  throw new ApiError("Operacao de prontuario nao suportada.", 400);
}

function handlePrescriptions<T>(
  db: LocalDb,
  segments: string[],
  url: URL,
  method: string,
  body: unknown,
  user: LocalUser,
): T {
  requireAnyRole(user, "admin", "medico", "farmaceutico");
  if (segments.length === 1 && method === "GET") {
    let items = [...db.prescriptions];
    const status = url.searchParams.get("status");
    if (status) {
      items = items.filter((item) => item.status === status);
    }
    if (user.role === "medico") {
      const recordIds = db.records.filter((record) => record.id_medico === user.id).map((record) => record.id);
      items = items.filter((item) => recordIds.includes(item.id_prontuario));
    }
    return paginate(enrichPrescriptions(db, items).sort(descBy("created_at")), url) as T;
  }
  if (segments.length === 1 && method === "POST") {
    requireRole(user, "medico");
    const data = body as { id_prontuario?: string; medicamentos?: string[]; itens?: PrescriptionItem[] };
    const created: Prescription = {
      id: newId(),
      id_prontuario: String(data.id_prontuario ?? ""),
      medicamentos: data.medicamentos?.length ? data.medicamentos : medicationLines(db, data.itens ?? []),
      status: "Pendente",
      created_at: now(),
    };
    db.prescriptions.push(created);
    replacePrescriptionItems(db, created.id, data.itens ?? []);
    audit(db, user, "prescription.create", "prescription", created.id);
    saveDb(db);
    return enrichPrescriptions(db, [created])[0] as T;
  }
  const id = segments[1];
  const prescription = db.prescriptions.find((item) => item.id === id);
  if (!prescription) {
    throw new ApiError("Prescricao nao encontrada.", 404);
  }
  if (segments[2] === "dispensar" && method === "PATCH") {
    requireRole(user, "farmaceutico");
    dispensePrescription(db, prescription, user);
    prescription.status = "Entregue";
    prescription.dispensed_at = now();
    audit(db, user, "prescription.dispense", "prescription", prescription.id);
    saveDb(db);
    return [prescription] as T;
  }
  if (method === "PATCH") {
    requireRole(user, "medico");
    const data = body as Partial<Prescription> & { itens?: PrescriptionItem[] };
    if (data.status) {
      prescription.status = data.status;
    }
    if (data.medicamentos) {
      prescription.medicamentos = data.medicamentos;
    }
    if (data.itens) {
      replacePrescriptionItems(db, prescription.id, data.itens);
      if (!data.medicamentos) {
        prescription.medicamentos = medicationLines(db, data.itens);
      }
    }
    audit(db, user, "prescription.update", "prescription", prescription.id);
    saveDb(db);
    return enrichPrescriptions(db, [prescription])[0] as T;
  }
  throw new ApiError("Operacao de prescricao nao suportada.", 400);
}

function handleMedications<T>(
  db: LocalDb,
  segments: string[],
  url: URL,
  method: string,
  body: unknown,
  user: LocalUser,
): T {
  requireAnyRole(user, "admin", "medico", "farmaceutico");
  if (segments[1] === "movimentacoes" && method === "GET") {
    requireAnyRole(user, "admin", "farmaceutico");
    let items = [...db.stockMovements];
    items = filterByParam(items, url, "id_medicamento");
    items = filterByParam(items, url, "tipo");
    return paginate(enrichStockMovements(db, items).sort(descBy("created_at")), url) as T;
  }
  if (segments.length === 1 && method === "GET") {
    let items = db.medications.map(enrichMedication);
    const ativo = url.searchParams.get("ativo");
    const baixoEstoque = url.searchParams.get("baixo_estoque");
    const search = url.searchParams.get("search");
    if (ativo) {
      items = items.filter((item) => item.ativo === (ativo === "true"));
    }
    if (baixoEstoque === "true") {
      items = items.filter((item) => item.baixo_estoque);
    }
    if (search) {
      items = items.filter((item) => item.nome.toLowerCase().includes(search.toLowerCase()));
    }
    return paginate(items.sort((a, b) => a.nome.localeCompare(b.nome)), url) as T;
  }
  if (segments.length === 1 && method === "POST") {
    requireAnyRole(user, "admin", "farmaceutico");
    const data = body as Partial<Medication>;
    const created: Medication = {
      id: newId(),
      nome: String(data.nome ?? ""),
      apresentacao: String(data.apresentacao ?? ""),
      quantidade: Number(data.quantidade ?? 0),
      estoque_minimo: Number(data.estoque_minimo ?? 0),
      ativo: data.ativo ?? true,
      baixo_estoque: false,
      created_at: now(),
      updated_at: now(),
    };
    db.medications.push(created);
    audit(db, user, "medication.create", "medication", created.id);
    saveDb(db);
    return enrichMedication(created) as T;
  }
  if (segments[2] === "movimentacoes" && method === "POST") {
    requireAnyRole(user, "admin", "farmaceutico");
    const medication = db.medications.find((item) => item.id === segments[1]);
    if (!medication) {
      throw new ApiError("Medicamento nao encontrado.", 404);
    }
    const data = body as Partial<StockMovement>;
    const previous = medication.quantidade;
    const quantity = Number(data.quantidade ?? 0);
    const next = data.tipo === "Saida" ? previous - quantity : previous + quantity;
    if (next < 0) {
      throw new ApiError("Estoque insuficiente para esta saida.", 400);
    }
    medication.quantidade = next;
    medication.updated_at = now();
    const movement: StockMovement = {
      id: newId(),
      id_medicamento: medication.id,
      tipo: data.tipo === "Saida" ? "Saida" : "Entrada",
      quantidade: quantity,
      quantidade_anterior: previous,
      quantidade_atual: next,
      observacoes: String(data.observacoes ?? ""),
      id_prescricao: data.id_prescricao,
      created_by: user.id,
      created_by_email: user.email,
      created_at: now(),
    };
    db.stockMovements.push(movement);
    audit(db, user, "medication.stock_movement", "medication", medication.id);
    saveDb(db);
    return enrichMedication(medication) as T;
  }
  throw new ApiError("Operacao de medicamento nao suportada.", 400);
}

function handleAppointments<T>(
  db: LocalDb,
  segments: string[],
  url: URL,
  method: string,
  body: unknown,
  user: LocalUser,
): T {
  requireAnyRole(user, "admin", "medico", "recepcao");
  if (segments.length === 1 && method === "GET") {
    let items = [...db.appointments];
    if (user.role === "medico") {
      items = items.filter((item) => item.id_medico === user.id);
    }
    items = filterByParam(items, url, "id_paciente");
    items = filterByParam(items, url, "id_medico");
    items = filterByParam(items, url, "status");
    items = filterByDate(items, url, "scheduled_at", "scheduled_from", "scheduled_to");
    return paginate(enrichAppointments(db, items).sort((a, b) => a.scheduled_at.localeCompare(b.scheduled_at)), url) as T;
  }
  if (segments.length === 1 && method === "POST") {
    requireAnyRole(user, "admin", "recepcao");
    const data = body as Partial<Appointment>;
    const created: Appointment = {
      id: newId(),
      id_paciente: String(data.id_paciente ?? ""),
      id_medico: String(data.id_medico ?? ""),
      scheduled_at: String(data.scheduled_at ?? now()),
      status: "Agendada",
      observacoes: String(data.observacoes ?? ""),
      created_at: now(),
      updated_at: now(),
    };
    db.appointments.push(created);
    audit(db, user, "appointment.create", "appointment", created.id);
    saveDb(db);
    return enrichAppointments(db, [created])[0] as T;
  }
  const appointment = db.appointments.find((item) => item.id === segments[1]);
  if (!appointment) {
    throw new ApiError("Consulta nao encontrada.", 404);
  }
  if (method === "PATCH") {
    const data = body as Partial<Appointment>;
    if (user.role === "medico") {
      appointment.status = data.status ?? appointment.status;
      appointment.observacoes = data.observacoes ?? appointment.observacoes;
    } else {
      Object.assign(appointment, data);
    }
    appointment.updated_at = now();
    audit(db, user, "appointment.update", "appointment", appointment.id, { status: appointment.status });
    saveDb(db);
    return enrichAppointments(db, [appointment])[0] as T;
  }
  throw new ApiError("Operacao de consulta nao suportada.", 400);
}

async function handleAttachments<T>(
  db: LocalDb,
  segments: string[],
  url: URL,
  method: string,
  body: unknown,
  form: FormData | undefined,
  user: LocalUser,
): Promise<T> {
  requireAnyRole(user, "admin", "medico", "recepcao");
  if (segments.length === 1 && method === "GET") {
    let items = [...db.attachments];
    items = filterByParam(items, url, "id_paciente");
    items = filterByParam(items, url, "id_prontuario");
    items = filterByParam(items, url, "tipo");
    return paginate(enrichAttachments(db, items).sort(descBy("created_at")), url) as T;
  }
  if (segments.length === 1 && method === "POST") {
    const data = body as Partial<ClinicalAttachment>;
    const created = createAttachmentRecord(db, user, {
      id_paciente: String(data.id_paciente ?? ""),
      id_prontuario: data.id_prontuario,
      tipo: data.tipo ?? "Outro",
      titulo: String(data.titulo ?? ""),
      arquivo_url: String(data.arquivo_url ?? ""),
      observacoes: String(data.observacoes ?? ""),
    });
    saveDb(db);
    return enrichAttachments(db, [created])[0] as T;
  }
  if (segments[1] === "upload" && method === "POST") {
    const file = form?.get("file");
    const dataUrl = file instanceof File ? await fileToDataUrl(file) : "";
    const created = createAttachmentRecord(db, user, {
      id_paciente: String(form?.get("id_paciente") ?? ""),
      id_prontuario: String(form?.get("id_prontuario") ?? "") || undefined,
      tipo: (String(form?.get("tipo") ?? "Outro") as AttachmentType),
      titulo: String(form?.get("titulo") ?? ""),
      arquivo_url: dataUrl,
      observacoes: String(form?.get("observacoes") ?? ""),
      file_name: file instanceof File ? file.name : undefined,
      content_type: file instanceof File ? file.type : undefined,
      file_size: file instanceof File ? file.size : undefined,
    });
    saveDb(db);
    return enrichAttachments(db, [created])[0] as T;
  }
  if (method === "DELETE") {
    requireRole(user, "admin");
    db.attachments = db.attachments.filter((item) => item.id !== segments[1]);
    audit(db, user, "attachment.delete", "attachment", segments[1]);
    saveDb(db);
    return { message: "Anexo removido." } as T;
  }
  throw new ApiError("Operacao de anexo nao suportada.", 400);
}

function handleUsers<T>(
  db: LocalDb,
  segments: string[],
  url: URL,
  method: string,
  body: unknown,
  user: LocalUser,
): T {
  if (segments[1] === "medicos" && method === "GET") {
    requireAnyRole(user, "admin", "medico", "recepcao");
    return db.users.filter((item) => item.role === "medico" && item.ativo).map(publicUser) as T;
  }
  requireRole(user, "admin");
  if (segments.length === 1 && method === "GET") {
    let items = db.users.map(publicUser);
    const search = url.searchParams.get("search");
    const role = url.searchParams.get("role");
    const ativo = url.searchParams.get("ativo");
    if (search) {
      items = items.filter((item) => item.email.toLowerCase().includes(search.toLowerCase()));
    }
    if (role) {
      items = items.filter((item) => item.role === role);
    }
    if (ativo) {
      items = items.filter((item) => item.ativo === (ativo === "true"));
    }
    return paginate(items.sort(descBy("created_at")), url) as T;
  }
  if (segments.length === 1 && method === "POST") {
    const data = body as Partial<LocalUser>;
    if (db.users.some((item) => item.email === data.email)) {
      throw new ApiError("E-mail ja cadastrado.", 400);
    }
    const created: LocalUser = {
      id: newId(),
      email: String(data.email ?? "").trim().toLowerCase(),
      senha: String(data.senha ?? "Senha@123"),
      role: data.role ?? "recepcao",
      nome: data.nome,
      ativo: data.ativo ?? true,
      created_at: now(),
      updated_at: now(),
    };
    db.users.push(created);
    audit(db, user, "user.create", "user", created.id, { target_email: created.email });
    saveDb(db);
    return publicUser(created) as T;
  }
  const target = db.users.find((item) => item.id === segments[1]);
  if (!target) {
    throw new ApiError("Usuario nao encontrado.", 404);
  }
  if (method === "PATCH") {
    const data = body as Partial<LocalUser>;
    target.email = data.email ? data.email.trim().toLowerCase() : target.email;
    target.nome = data.nome ?? target.nome;
    target.role = data.role ?? target.role;
    target.ativo = data.ativo ?? target.ativo;
    target.senha = data.senha || target.senha;
    target.updated_at = now();
    audit(db, user, "user.update", "user", target.id, { target_email: target.email });
    saveDb(db);
    return publicUser(target) as T;
  }
  return publicUser(target) as T;
}

function createAttachmentRecord(
  db: LocalDb,
  user: LocalUser,
  data: {
    id_paciente: string;
    id_prontuario?: string | null;
    tipo: AttachmentType;
    titulo: string;
    arquivo_url: string;
    observacoes: string;
    file_name?: string;
    content_type?: string;
    file_size?: number;
  },
): ClinicalAttachment {
  const created: ClinicalAttachment = {
    id: newId(),
    id_paciente: data.id_paciente,
    id_prontuario: data.id_prontuario || undefined,
    tipo: data.tipo,
    titulo: data.titulo,
    arquivo_url: data.arquivo_url,
    download_url: data.arquivo_url,
    observacoes: data.observacoes,
    file_name: data.file_name,
    content_type: data.content_type,
    file_size: data.file_size,
    uploaded_by: user.id,
    uploaded_by_email: user.email,
    created_at: now(),
    updated_at: now(),
  };
  db.attachments.push(created);
  audit(db, user, "attachment.create", "attachment", created.id);
  return created;
}

function dispensePrescription(db: LocalDb, prescription: Prescription, user: LocalUser) {
  const items = db.prescriptionItems.filter((item) => item.id_prescricao === prescription.id);
  for (const item of items) {
    const medication = db.medications.find((entry) => entry.id === item.id_medicamento);
    if (!medication) {
      throw new ApiError("Medicamento da prescricao nao encontrado.", 404);
    }
    if (medication.quantidade < item.quantidade) {
      throw new ApiError(`Estoque insuficiente para ${medication.nome}.`, 400);
    }
  }
  for (const item of items) {
    const medication = db.medications.find((entry) => entry.id === item.id_medicamento);
    if (!medication) {
      continue;
    }
    const previous = medication.quantidade;
    medication.quantidade -= item.quantidade;
    medication.updated_at = now();
    db.stockMovements.push({
      id: newId(),
      id_medicamento: medication.id,
      tipo: "Saida",
      quantidade: item.quantidade,
      quantidade_anterior: previous,
      quantidade_atual: medication.quantidade,
      observacoes: "Baixa automatica por dispensacao de prescricao.",
      id_prescricao: prescription.id,
      created_by: user.id,
      created_by_email: user.email,
      created_at: now(),
    });
  }
}

function replacePrescriptionItems(db: LocalDb, idPrescricao: string, items: PrescriptionItem[]) {
  db.prescriptionItems = db.prescriptionItems.filter((item) => item.id_prescricao !== idPrescricao);
  db.prescriptionItems.push(
    ...items.map((item) => ({
      id: newId(),
      id_prescricao: idPrescricao,
      id_medicamento: item.id_medicamento,
      quantidade: Number(item.quantidade),
      posologia: item.posologia,
      created_at: now(),
    })),
  );
}

function medicationLines(db: LocalDb, items: PrescriptionItem[]) {
  return items.map((item) => {
    const medication = db.medications.find((entry) => entry.id === item.id_medicamento);
    const label = medication ? `${medication.nome} ${medication.apresentacao}`.trim() : item.id_medicamento;
    return `${label} - qtd. ${item.quantidade} - ${item.posologia}`;
  });
}

function enrichRecords(db: LocalDb, records: MedicalRecord[]) {
  return records.map((record) => {
    const patient = db.patients.find((item) => item.id === record.id_paciente);
    const doctor = db.users.find((item) => item.id === record.id_medico);
    const appointment = record.id_consulta ? db.appointments.find((item) => item.id === record.id_consulta) : null;
    return {
      ...record,
      paciente_nome: patient?.nome,
      medico_nome: doctor?.nome || doctor?.email,
      consulta_status: appointment?.status,
      consulta_scheduled_at: appointment?.scheduled_at,
    };
  });
}

function enrichPrescriptions(db: LocalDb, prescriptions: Prescription[]) {
  return prescriptions.map((prescription) => {
    const record = db.records.find((item) => item.id === prescription.id_prontuario);
    const patient = record ? db.patients.find((item) => item.id === record.id_paciente) : null;
    const doctor = record ? db.users.find((item) => item.id === record.id_medico) : null;
    const items = db.prescriptionItems
      .filter((item) => item.id_prescricao === prescription.id)
      .map((item) => {
        const medication = db.medications.find((entry) => entry.id === item.id_medicamento);
        return {
          ...item,
          medicamento_nome: medication?.nome,
          medicamento_apresentacao: medication?.apresentacao,
        };
      });
    return {
      ...prescription,
      id_paciente: record?.id_paciente,
      id_medico: record?.id_medico,
      paciente_nome: patient?.nome,
      medico_nome: doctor?.nome || doctor?.email,
      diagnostico: record?.diagnostico,
      prontuario_created_at: record?.created_at,
      itens: items,
    };
  });
}

function enrichAppointments(db: LocalDb, appointments: Appointment[]) {
  return appointments.map((appointment) => {
    const patient = db.patients.find((item) => item.id === appointment.id_paciente);
    const doctor = db.users.find((item) => item.id === appointment.id_medico);
    return {
      ...appointment,
      paciente_nome: patient?.nome,
      medico_nome: doctor?.nome || doctor?.email,
    };
  });
}

function enrichAttachments(db: LocalDb, attachments: ClinicalAttachment[]) {
  return attachments.map((attachment) => {
    const patient = db.patients.find((item) => item.id === attachment.id_paciente);
    const record = attachment.id_prontuario ? db.records.find((item) => item.id === attachment.id_prontuario) : null;
    return {
      ...attachment,
      paciente_nome: patient?.nome,
      prontuario_diagnostico: record?.diagnostico,
      download_url: attachment.download_url || attachment.arquivo_url,
    };
  });
}

function enrichMedication(medication: Medication): Medication {
  return {
    ...medication,
    baixo_estoque: medication.quantidade <= medication.estoque_minimo,
  };
}

function enrichStockMovements(db: LocalDb, movements: StockMovement[]) {
  return movements.map((movement) => {
    const medication = db.medications.find((item) => item.id === movement.id_medicamento);
    return {
      ...movement,
      medicamento_nome: medication?.nome,
      medicamento_apresentacao: medication?.apresentacao,
    };
  });
}

function buildReport(db: LocalDb, url: URL): IndicatorsReport {
  const createdFrom = url.searchParams.get("created_from");
  const createdTo = url.searchParams.get("created_to");
  const patients = filterDateRange(db.patients, "created_at", createdFrom, createdTo);
  const records = filterDateRange(db.records, "created_at", createdFrom, createdTo);
  const prescriptions = filterDateRange(db.prescriptions, "created_at", createdFrom, createdTo);
  const appointments = filterDateRange(db.appointments, "scheduled_at", createdFrom, createdTo);
  const stockMovements = filterDateRange(db.stockMovements, "created_at", createdFrom, createdTo);
  const prescriptionStatuses = countBy(prescriptions, "status");
  const appointmentStatuses = countBy(appointments, "status");
  const stockMovementTypes = countBy(stockMovements, "tipo");
  const diagnoses = countLabels(records.map((item) => item.diagnostico).filter(Boolean));

  return {
    period: {
      created_from: createdFrom,
      created_to: createdTo,
    },
    totals: {
      pacientes: patients.length,
      prontuarios: records.length,
      prescricoes: prescriptions.length,
      prescricoes_pendentes: prescriptionStatuses.Pendente ?? 0,
      consultas: appointments.length,
      consultas_agendadas: appointmentStatuses.Agendada ?? 0,
      consultas_realizadas: appointmentStatuses.Realizada ?? 0,
      consultas_canceladas: appointmentStatuses.Cancelada ?? 0,
      medicamentos: db.medications.length,
      medicamentos_baixo_estoque: db.medications.filter((item) => enrichMedication(item).baixo_estoque).length,
      movimentacoes_estoque: stockMovements.length,
      usuarios_ativos: db.users.filter((item) => item.ativo).length,
      usuarios_inativos: db.users.filter((item) => !item.ativo).length,
    },
    prescriptions_by_status: bucketFromLabels(["Pendente", "Entregue", "Cancelada"], prescriptionStatuses),
    appointments_by_status: bucketFromLabels(["Agendada", "Realizada", "Cancelada"], appointmentStatuses),
    stock_movements_by_type: bucketFromLabels(["Entrada", "Saida"], stockMovementTypes),
    patients_by_month: bucketByDate(patients, "created_at", "month"),
    records_by_day: bucketByDate(records, "created_at", "day"),
    appointments_by_day: bucketByDate(appointments, "scheduled_at", "day"),
    stock_movements_by_day: bucketByDate(stockMovements, "created_at", "day"),
    top_diagnoses: Object.entries(diagnoses)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([label, value]) => ({ label, value })),
  };
}

function reportToCsv(report: IndicatorsReport) {
  const rows = [
    ["Sistema de Prontuarios - Relatorio de Indicadores"],
    ["Periodo inicial", report.period.created_from || "inicio"],
    ["Periodo final", report.period.created_to || "hoje"],
    [],
    ["Totais"],
    ...Object.entries(report.totals).map(([key, value]) => [key, String(value)]),
  ];
  return rows.map((row) => row.join(";")).join("\n");
}

function filterAudit(items: AuditLog[], url: URL) {
  let result = [...items];
  result = filterByParam(result, url, "action");
  result = filterByParam(result, url, "resource_type");
  const actorEmail = url.searchParams.get("actor_email");
  if (actorEmail) {
    result = result.filter((item) => item.actor_email.toLowerCase().includes(actorEmail.toLowerCase()));
  }
  return filterByDate(result, url, "created_at", "created_from", "created_to").sort(descBy("created_at"));
}

function audit(
  db: LocalDb,
  user: LocalUser,
  action: string,
  resourceType: string,
  resourceId?: string,
  metadata: Record<string, unknown> = {},
) {
  db.auditLogs.push({
    id: newId(),
    actor_id: user.id,
    actor_email: user.email,
    actor_role: user.role,
    action,
    resource_type: resourceType,
    resource_id: resourceId,
    metadata,
    created_at: now(),
  });
}

function paginate<T>(items: T[], url: URL): PaginatedResponse<T> {
  const limit = Number(url.searchParams.get("limit") ?? 20);
  const offset = Number(url.searchParams.get("offset") ?? 0);
  return {
    items: items.slice(offset, offset + limit),
    limit,
    offset,
  };
}

function filterByParam<T extends Record<string, unknown>>(items: T[], url: URL, key: string) {
  const value = url.searchParams.get(key);
  return value ? items.filter((item) => String(item[key]) === value) : items;
}

function filterByDate<T extends Record<string, unknown>>(
  items: T[],
  url: URL,
  field: string,
  fromKey: string,
  toKey: string,
) {
  return filterDateRange(items, field, url.searchParams.get(fromKey), url.searchParams.get(toKey));
}

function filterDateRange<T extends Record<string, unknown>>(items: T[], field: string, from?: string | null, to?: string | null) {
  return items.filter((item) => {
    const value = String(item[field] ?? "");
    if (from && value.slice(0, 10) < from) {
      return false;
    }
    if (to && value.slice(0, 10) > to) {
      return false;
    }
    return true;
  });
}

function bucketFromLabels(labels: string[], counts: Record<string, number>) {
  return labels.map((label) => ({ label, value: counts[label] ?? 0 }));
}

function bucketByDate<T extends Record<string, unknown>>(items: T[], field: string, mode: "day" | "month") {
  const counts: Record<string, number> = {};
  for (const item of items) {
    const value = String(item[field] ?? "");
    const label = mode === "month" ? value.slice(0, 7) : value.slice(0, 10);
    if (label) {
      counts[label] = (counts[label] ?? 0) + 1;
    }
  }
  return Object.entries(counts)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([label, value]) => ({ label, value }));
}

function countBy<T extends Record<string, unknown>>(items: T[], field: string) {
  const counts: Record<string, number> = {};
  for (const item of items) {
    const key = String(item[field] ?? "");
    counts[key] = (counts[key] ?? 0) + 1;
  }
  return counts;
}

function countLabels(labels: string[]) {
  const counts: Record<string, number> = {};
  for (const label of labels) {
    counts[label] = (counts[label] ?? 0) + 1;
  }
  return counts;
}

function publicUser(user: LocalUser): AppUser {
  const { senha, ...publicData } = user;
  return publicData;
}

function publicCurrentUser(user: LocalUser): CurrentUser {
  return {
    id: user.id,
    email: user.email,
    role: user.role,
  };
}

function currentUserFromToken(db: LocalDb, token?: string) {
  const payload = decodeToken(token);
  const user = payload ? db.users.find((item) => item.id === payload.id) : null;
  if (!user || !user.ativo) {
    throw new ApiError("Token invalido.", 401);
  }
  return user;
}

function encodeToken(user: LocalUser) {
  return `${TOKEN_PREFIX}${btoa(JSON.stringify(publicCurrentUser(user)))}`;
}

function decodeToken(token?: string): TokenPayload | null {
  if (!token?.startsWith(TOKEN_PREFIX)) {
    return null;
  }
  try {
    return JSON.parse(atob(token.slice(TOKEN_PREFIX.length))) as TokenPayload;
  } catch {
    return null;
  }
}

function requireRole(user: LocalUser, role: UserRole) {
  if (user.role !== role) {
    throw new ApiError(`Permissao negada. Perfil necessario: ${role}.`, 403);
  }
}

function requireAnyRole(user: LocalUser, ...roles: UserRole[]) {
  if (!roles.includes(user.role)) {
    throw new ApiError(`Permissao negada. Perfil necessario: ${roles.join(", ")}.`, 403);
  }
}

function loadDb(): LocalDb {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    const db = clone(seedDb);
    saveDb(db);
    return db;
  }
  return JSON.parse(raw) as LocalDb;
}

function saveDb(db: LocalDb) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(db));
}

function clone<T>(value: T): T {
  return JSON.parse(JSON.stringify(value)) as T;
}

function newId() {
  return crypto.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function now() {
  return new Date().toISOString();
}

function onlyDigits(value: string) {
  return value.replace(/\D+/g, "");
}

function descBy<T extends Record<string, unknown>>(field: string) {
  return (a: T, b: T) => String(b[field] ?? "").localeCompare(String(a[field] ?? ""));
}

function enrichPatient(patient: Patient) {
  return patient;
}

function fileToDataUrl(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result ?? ""));
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });
}
