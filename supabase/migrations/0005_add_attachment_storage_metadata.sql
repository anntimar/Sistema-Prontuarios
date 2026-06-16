alter table public.clinical_attachments
add column if not exists storage_bucket text,
add column if not exists storage_path text,
add column if not exists file_name text,
add column if not exists content_type text,
add column if not exists file_size bigint;

alter table public.clinical_attachments
drop constraint if exists clinical_attachments_file_size_check;

alter table public.clinical_attachments
add constraint clinical_attachments_file_size_check
check (file_size is null or file_size >= 0);

create index if not exists idx_clinical_attachments_storage_path
on public.clinical_attachments(storage_path);

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
