create extension if not exists "pgcrypto";
create extension if not exists "citext";

create table if not exists public.clinical_attachments (
    id uuid primary key default gen_random_uuid(),
    id_paciente uuid not null references public.pacientes(id) on delete cascade,
    id_prontuario uuid references public.medical_records(id) on delete set null,
    tipo text not null check (tipo in ('Exame', 'Laudo', 'Imagem', 'Outro')),
    titulo text not null,
    arquivo_url text not null,
    observacoes text not null default '',
    uploaded_by text,
    uploaded_by_email citext,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index if not exists idx_clinical_attachments_paciente on public.clinical_attachments(id_paciente);
create index if not exists idx_clinical_attachments_prontuario on public.clinical_attachments(id_prontuario);
create index if not exists idx_clinical_attachments_tipo on public.clinical_attachments(tipo);
create index if not exists idx_clinical_attachments_created_at on public.clinical_attachments(created_at desc);

create or replace function public.set_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

drop trigger if exists set_clinical_attachments_updated_at on public.clinical_attachments;
create trigger set_clinical_attachments_updated_at
before update on public.clinical_attachments
for each row execute function public.set_updated_at();
