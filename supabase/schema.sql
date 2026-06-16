create extension if not exists "pgcrypto";
create extension if not exists "citext";

create table if not exists public.users (
    id uuid primary key default gen_random_uuid(),
    email citext not null unique,
    password_hash text not null,
    role text not null check (role in ('admin', 'medico', 'farmaceutico', 'recepcao')),
    nome text,
    ativo boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.pacientes (
    id uuid primary key default gen_random_uuid(),
    nome text not null,
    cpf char(11) not null unique check (cpf ~ '^[0-9]{11}$'),
    data_nascimento date not null,
    telefone varchar(11) not null check (telefone ~ '^[0-9]{10,11}$'),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.appointments (
    id uuid primary key default gen_random_uuid(),
    id_paciente uuid not null references public.pacientes(id) on delete cascade,
    id_medico uuid not null references public.users(id),
    scheduled_at timestamptz not null,
    status text not null default 'Agendada' check (status in ('Agendada', 'Realizada', 'Cancelada')),
    observacoes text not null default '',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.medical_records (
    id uuid primary key default gen_random_uuid(),
    id_paciente uuid not null references public.pacientes(id) on delete cascade,
    id_medico uuid not null references public.users(id),
    id_consulta uuid unique references public.appointments(id),
    anamnese text not null,
    diagnostico text not null,
    observacoes text not null default '',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.prescriptions (
    id uuid primary key default gen_random_uuid(),
    id_prontuario uuid not null references public.medical_records(id) on delete cascade,
    medicamentos jsonb not null default '[]'::jsonb,
    status text not null default 'Pendente' check (status in ('Pendente', 'Entregue', 'Cancelada')),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    dispensed_at timestamptz
);

create table if not exists public.medications (
    id uuid primary key default gen_random_uuid(),
    nome text not null,
    apresentacao text not null,
    quantidade integer not null default 0 check (quantidade >= 0),
    estoque_minimo integer not null default 0 check (estoque_minimo >= 0),
    ativo boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.medication_movements (
    id uuid primary key default gen_random_uuid(),
    id_medicamento uuid not null references public.medications(id) on delete cascade,
    tipo text not null check (tipo in ('Entrada', 'Saida')),
    quantidade integer not null check (quantidade > 0),
    quantidade_anterior integer not null check (quantidade_anterior >= 0),
    quantidade_atual integer not null check (quantidade_atual >= 0),
    observacoes text not null default '',
    id_prescricao uuid references public.prescriptions(id) on delete set null,
    created_by text,
    created_by_email citext,
    created_at timestamptz not null default now()
);

create table if not exists public.prescription_items (
    id uuid primary key default gen_random_uuid(),
    id_prescricao uuid not null references public.prescriptions(id) on delete cascade,
    id_medicamento uuid not null references public.medications(id) on delete restrict,
    quantidade integer not null check (quantidade > 0),
    posologia text not null,
    created_at timestamptz not null default now()
);

create table if not exists public.clinical_attachments (
    id uuid primary key default gen_random_uuid(),
    id_paciente uuid not null references public.pacientes(id) on delete cascade,
    id_prontuario uuid references public.medical_records(id) on delete set null,
    tipo text not null check (tipo in ('Exame', 'Laudo', 'Imagem', 'Outro')),
    titulo text not null,
    arquivo_url text not null,
    observacoes text not null default '',
    storage_bucket text,
    storage_path text,
    file_name text,
    content_type text,
    file_size bigint check (file_size is null or file_size >= 0),
    uploaded_by text,
    uploaded_by_email citext,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.audit_logs (
    id uuid primary key default gen_random_uuid(),
    actor_id text,
    actor_email citext not null,
    actor_role text not null,
    action text not null,
    resource_type text not null,
    resource_id text,
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create index if not exists idx_pacientes_nome on public.pacientes using gin (to_tsvector('portuguese', nome));
create index if not exists idx_pacientes_cpf on public.pacientes(cpf);
create index if not exists idx_appointments_paciente on public.appointments(id_paciente);
create index if not exists idx_appointments_medico on public.appointments(id_medico);
create index if not exists idx_appointments_status on public.appointments(status);
create index if not exists idx_appointments_scheduled_at on public.appointments(scheduled_at);
create index if not exists idx_medical_records_paciente on public.medical_records(id_paciente);
create index if not exists idx_medical_records_medico on public.medical_records(id_medico);
create index if not exists idx_medical_records_consulta on public.medical_records(id_consulta);
create index if not exists idx_prescriptions_prontuario on public.prescriptions(id_prontuario);
create index if not exists idx_prescriptions_status on public.prescriptions(status);
create index if not exists idx_medications_nome on public.medications using gin (to_tsvector('portuguese', nome));
create index if not exists idx_medications_ativo on public.medications(ativo);
create index if not exists idx_medications_low_stock on public.medications(quantidade, estoque_minimo);
create index if not exists idx_medication_movements_medicamento on public.medication_movements(id_medicamento);
create index if not exists idx_medication_movements_prescricao on public.medication_movements(id_prescricao);
create index if not exists idx_medication_movements_created_at on public.medication_movements(created_at desc);
create index if not exists idx_prescription_items_prescricao on public.prescription_items(id_prescricao);
create index if not exists idx_prescription_items_medicamento on public.prescription_items(id_medicamento);
create index if not exists idx_clinical_attachments_paciente on public.clinical_attachments(id_paciente);
create index if not exists idx_clinical_attachments_prontuario on public.clinical_attachments(id_prontuario);
create index if not exists idx_clinical_attachments_tipo on public.clinical_attachments(tipo);
create index if not exists idx_clinical_attachments_created_at on public.clinical_attachments(created_at desc);
create index if not exists idx_clinical_attachments_storage_path on public.clinical_attachments(storage_path);
create index if not exists idx_audit_logs_created_at on public.audit_logs(created_at desc);
create index if not exists idx_audit_logs_actor_email on public.audit_logs(actor_email);
create index if not exists idx_audit_logs_action on public.audit_logs(action);
create index if not exists idx_audit_logs_resource on public.audit_logs(resource_type, resource_id);

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
    'clinical-attachments',
    'clinical-attachments',
    false,
    10485760,
    array['application/pdf', 'image/jpeg', 'image/png', 'image/webp']::text[]
)
on conflict (id) do update set
    public = excluded.public,
    file_size_limit = excluded.file_size_limit,
    allowed_mime_types = excluded.allowed_mime_types;

create or replace function public.set_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

drop trigger if exists set_users_updated_at on public.users;
create trigger set_users_updated_at
before update on public.users
for each row execute function public.set_updated_at();

drop trigger if exists set_pacientes_updated_at on public.pacientes;
create trigger set_pacientes_updated_at
before update on public.pacientes
for each row execute function public.set_updated_at();

drop trigger if exists set_medical_records_updated_at on public.medical_records;
create trigger set_medical_records_updated_at
before update on public.medical_records
for each row execute function public.set_updated_at();

drop trigger if exists set_prescriptions_updated_at on public.prescriptions;
create trigger set_prescriptions_updated_at
before update on public.prescriptions
for each row execute function public.set_updated_at();

drop trigger if exists set_medications_updated_at on public.medications;
create trigger set_medications_updated_at
before update on public.medications
for each row execute function public.set_updated_at();

drop trigger if exists set_clinical_attachments_updated_at on public.clinical_attachments;
create trigger set_clinical_attachments_updated_at
before update on public.clinical_attachments
for each row execute function public.set_updated_at();

drop trigger if exists set_appointments_updated_at on public.appointments;
create trigger set_appointments_updated_at
before update on public.appointments
for each row execute function public.set_updated_at();
