insert into public.users (id, email, password_hash, role, nome)
values
    (
        '00000000-0000-0000-0000-000000000010',
        'admin@hospital.com',
        '$2b$12$810O/073osR4GfJmc0w3Qeiihoy11MqgUO2QbacJqBL.HK56aDoUW',
        'admin',
        'Administrador Padrao'
    ),
    (
        '00000000-0000-0000-0000-000000000001',
        'medico@hospital.com',
        '$2b$12$eInX1f8zoU0zY86qfrFc6OPiHLdgc9rmlho68s2VwYaTeOY80c0IS',
        'medico',
        'Medico Padrao'
    ),
    (
        '00000000-0000-0000-0000-000000000002',
        'farmacia@hospital.com',
        '$2b$12$u0DfBerITdUBJv1oiJer6eO3MYbfcWhfijxf4JL23NivoXv/B5a.K',
        'farmaceutico',
        'Farmacia Padrao'
    ),
    (
        '00000000-0000-0000-0000-000000000003',
        'recepcao@hospital.com',
        '$2b$12$lBcTba.t0/lgGH3.e2I6dOO7tGxZRqp8xyBU9d9vAi39SxuPtVasu',
        'recepcao',
        'Recepcao Padrao'
    )
on conflict (email) do update set
    password_hash = excluded.password_hash,
    role = excluded.role,
    nome = excluded.nome,
    ativo = true;

insert into public.pacientes (id, nome, cpf, data_nascimento, telefone)
values
    (
        '10000000-0000-0000-0000-000000000001',
        'Joao da Silva',
        '12345678900',
        '1990-05-15',
        '82999999999'
    ),
    (
        '10000000-0000-0000-0000-000000000002',
        'Maria Oliveira',
        '09876543211',
        '1985-10-22',
        '82988888888'
    )
on conflict (cpf) do nothing;

insert into public.appointments (
    id,
    id_paciente,
    id_medico,
    scheduled_at,
    status,
    observacoes
)
values
    (
        '40000000-0000-0000-0000-000000000001',
        '10000000-0000-0000-0000-000000000001',
        '00000000-0000-0000-0000-000000000001',
        now() - interval '1 day',
        'Realizada',
        'Consulta inicial de acompanhamento.'
    ),
    (
        '40000000-0000-0000-0000-000000000002',
        '10000000-0000-0000-0000-000000000002',
        '00000000-0000-0000-0000-000000000001',
        now() + interval '1 day',
        'Agendada',
        'Retorno ambulatorial.'
    )
on conflict (id) do nothing;

insert into public.medical_records (
    id,
    id_paciente,
    id_medico,
    id_consulta,
    anamnese,
    diagnostico,
    observacoes
)
values (
    '20000000-0000-0000-0000-000000000001',
    '10000000-0000-0000-0000-000000000001',
    '00000000-0000-0000-0000-000000000001',
    '40000000-0000-0000-0000-000000000001',
    'Paciente relata dor de cabeca recorrente ha tres dias.',
    'Cefaleia tensional',
    'Orientado repouso, hidratacao e retorno em caso de piora.'
)
on conflict (id) do nothing;

insert into public.prescriptions (id, id_prontuario, medicamentos, status)
values (
    '30000000-0000-0000-0000-000000000001',
    '20000000-0000-0000-0000-000000000001',
    '["Dipirona 500mg a cada 6 horas se dor"]'::jsonb,
    'Pendente'
)
on conflict (id) do nothing;

insert into public.medications (
    id,
    nome,
    apresentacao,
    quantidade,
    estoque_minimo,
    ativo
)
values
    (
        '60000000-0000-0000-0000-000000000001',
        'Dipirona',
        '500mg',
        120,
        20,
        true
    ),
    (
        '60000000-0000-0000-0000-000000000002',
        'Ibuprofeno',
        '400mg',
        12,
        15,
        true
    ),
    (
        '60000000-0000-0000-0000-000000000003',
        'Amoxicilina',
        '500mg',
        40,
        10,
        true
    )
on conflict (id) do nothing;

insert into public.prescription_items (
    id,
    id_prescricao,
    id_medicamento,
    quantidade,
    posologia
)
values (
    '70000000-0000-0000-0000-000000000001',
    '30000000-0000-0000-0000-000000000001',
    '60000000-0000-0000-0000-000000000001',
    1,
    'Tomar 1 comprimido a cada 6 horas se dor.'
)
on conflict (id) do nothing;

insert into public.clinical_attachments (
    id,
    id_paciente,
    id_prontuario,
    tipo,
    titulo,
    arquivo_url,
    observacoes,
    uploaded_by,
    uploaded_by_email
)
values (
    '50000000-0000-0000-0000-000000000001',
    '10000000-0000-0000-0000-000000000001',
    '20000000-0000-0000-0000-000000000001',
    'Exame',
    'Hemograma de exemplo',
    'https://example.com/exames/hemograma-exemplo.pdf',
    'Arquivo demonstrativo para validar o fluxo de anexos clinicos.',
    '00000000-0000-0000-0000-000000000001',
    'medico@hospital.com'
)
on conflict (id) do nothing;
