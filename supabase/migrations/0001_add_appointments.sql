create extension if not exists "pgcrypto";

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

create index if not exists idx_appointments_paciente on public.appointments(id_paciente);
create index if not exists idx_appointments_medico on public.appointments(id_medico);
create index if not exists idx_appointments_status on public.appointments(status);
create index if not exists idx_appointments_scheduled_at on public.appointments(scheduled_at);

create or replace function public.set_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

drop trigger if exists set_appointments_updated_at on public.appointments;
create trigger set_appointments_updated_at
before update on public.appointments
for each row execute function public.set_updated_at();
