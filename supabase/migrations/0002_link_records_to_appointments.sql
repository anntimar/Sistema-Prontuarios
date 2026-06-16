alter table public.medical_records
add column if not exists id_consulta uuid;

do $$
begin
    if not exists (
        select 1
        from pg_constraint
        where conname = 'medical_records_id_consulta_fkey'
    ) then
        alter table public.medical_records
        add constraint medical_records_id_consulta_fkey
        foreign key (id_consulta) references public.appointments(id);
    end if;
end;
$$;

create unique index if not exists idx_medical_records_consulta_unique
on public.medical_records(id_consulta)
where id_consulta is not null;

create index if not exists idx_medical_records_consulta
on public.medical_records(id_consulta);
