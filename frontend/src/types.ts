export type Patient = {
  id: string;
  nome: string;
  cpf: string;
  data_nascimento: string;
  telefone: string;
  created_at?: string;
};

export type MedicalRecord = {
  id: string;
  id_paciente: string;
  id_medico: string;
  id_consulta?: string | null;
  anamnese: string;
  diagnostico: string;
  observacoes: string;
  paciente_nome?: string | null;
  medico_nome?: string | null;
  consulta_status?: AppointmentStatus | null;
  consulta_scheduled_at?: string | null;
  created_at?: string;
};

export type PrescriptionItem = {
  id?: string;
  id_prescricao?: string;
  id_medicamento: string;
  quantidade: number;
  posologia: string;
  medicamento_nome?: string | null;
  medicamento_apresentacao?: string | null;
  created_at?: string;
};

export type Prescription = {
  id: string;
  id_prontuario: string;
  id_paciente?: string;
  id_medico?: string;
  medicamentos: string[];
  itens?: PrescriptionItem[];
  status: "Pendente" | "Entregue" | "Cancelada";
  paciente_nome?: string | null;
  medico_nome?: string | null;
  diagnostico?: string | null;
  prontuario_created_at?: string;
  created_at?: string;
  dispensed_at?: string;
};

export type Medication = {
  id: string;
  nome: string;
  apresentacao: string;
  quantidade: number;
  estoque_minimo: number;
  ativo: boolean;
  baixo_estoque: boolean;
  created_at?: string;
  updated_at?: string;
};

export type StockMovement = {
  id: string;
  id_medicamento: string;
  tipo: "Entrada" | "Saida";
  quantidade: number;
  quantidade_anterior: number;
  quantidade_atual: number;
  observacoes: string;
  id_prescricao?: string | null;
  created_by?: string | null;
  created_by_email?: string | null;
  medicamento_nome?: string | null;
  medicamento_apresentacao?: string | null;
  created_at?: string;
};

export type AppointmentStatus = "Agendada" | "Realizada" | "Cancelada";

export type Appointment = {
  id: string;
  id_paciente: string;
  id_medico: string;
  scheduled_at: string;
  status: AppointmentStatus;
  observacoes: string;
  paciente_nome?: string | null;
  medico_nome?: string | null;
  created_at?: string;
  updated_at?: string;
};

export type AttachmentType = "Exame" | "Laudo" | "Imagem" | "Outro";

export type ClinicalAttachment = {
  id: string;
  id_paciente: string;
  id_prontuario?: string | null;
  tipo: AttachmentType;
  titulo: string;
  arquivo_url: string;
  observacoes: string;
  download_url?: string | null;
  storage_bucket?: string | null;
  storage_path?: string | null;
  file_name?: string | null;
  content_type?: string | null;
  file_size?: number | null;
  paciente_nome?: string | null;
  prontuario_diagnostico?: string | null;
  uploaded_by?: string | null;
  uploaded_by_email?: string | null;
  created_at?: string;
  updated_at?: string;
};

export type UserRole = "admin" | "medico" | "farmaceutico" | "recepcao";

export type AppUser = {
  id: string;
  email: string;
  role: UserRole;
  nome?: string | null;
  ativo: boolean;
  created_at?: string;
  updated_at?: string;
};

export type CurrentUser = {
  id: string;
  email: string;
  role: UserRole;
};

export type AuditLog = {
  id: string;
  actor_id?: string | null;
  actor_email: string;
  actor_role: string;
  action: string;
  resource_type: string;
  resource_id?: string | null;
  metadata: Record<string, unknown>;
  created_at?: string;
};

export type ReportBucket = {
  label: string;
  value: number;
};

export type IndicatorsReport = {
  period: {
    created_from?: string | null;
    created_to?: string | null;
  };
  totals: {
    pacientes: number;
    prontuarios: number;
    prescricoes: number;
    prescricoes_pendentes: number;
    consultas: number;
    consultas_agendadas: number;
    consultas_realizadas: number;
    consultas_canceladas: number;
    medicamentos: number;
    medicamentos_baixo_estoque: number;
    movimentacoes_estoque: number;
    usuarios_ativos: number;
    usuarios_inativos: number;
  };
  prescriptions_by_status: ReportBucket[];
  appointments_by_status: ReportBucket[];
  stock_movements_by_type: ReportBucket[];
  patients_by_month: ReportBucket[];
  records_by_day: ReportBucket[];
  appointments_by_day: ReportBucket[];
  stock_movements_by_day: ReportBucket[];
  top_diagnoses: ReportBucket[];
};

export type PaginatedResponse<T> = {
  items: T[];
  limit: number;
  offset: number;
};
