create table if not exists public.prescription_items (
    id uuid primary key default gen_random_uuid(),
    id_prescricao uuid not null references public.prescriptions(id) on delete cascade,
    id_medicamento uuid not null references public.medications(id) on delete restrict,
    quantidade integer not null check (quantidade > 0),
    posologia text not null,
    created_at timestamptz not null default now()
);

create index if not exists idx_prescription_items_prescricao
on public.prescription_items(id_prescricao);

create index if not exists idx_prescription_items_medicamento
on public.prescription_items(id_medicamento);
