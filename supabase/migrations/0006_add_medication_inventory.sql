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

create index if not exists idx_medications_nome on public.medications using gin (to_tsvector('portuguese', nome));
create index if not exists idx_medications_ativo on public.medications(ativo);
create index if not exists idx_medications_low_stock on public.medications(quantidade, estoque_minimo);
create index if not exists idx_medication_movements_medicamento on public.medication_movements(id_medicamento);
create index if not exists idx_medication_movements_prescricao on public.medication_movements(id_prescricao);
create index if not exists idx_medication_movements_created_at on public.medication_movements(created_at desc);

create or replace function public.set_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

drop trigger if exists set_medications_updated_at on public.medications;
create trigger set_medications_updated_at
before update on public.medications
for each row execute function public.set_updated_at();
