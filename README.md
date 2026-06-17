# Sistema-Prontuarios

Sistema full stack para gestao de pacientes, prontuarios medicos, prescricoes, consultas e anexos clinicos.
Por padrao ele roda com banco local em JSON, sem precisar criar Supabase nem configurar chaves.

## Stack atual

- Python 3.12
- FastAPI
- JSON local
- JWT
- bcrypt
- React
- Docker
- Nginx

## Como configurar

Fluxo automatico recomendado:

```powershell
.\scripts\setup_dev.ps1
```

O `.env.example` ja vem com `DATA_BACKEND=json`, que usa a base local em
`backend/data/local_db.json`. A primeira execucao cria esse arquivo a partir de
`backend/data/local_seed.json`.

Para criar o `.env` local:

```powershell
Copy-Item .env.example .env
```

Para restaurar os dados de demonstracao:

```powershell
.\scripts\reset_local_data.ps1
```

Fluxo manual:

Crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
python -m pip install -r requirements.txt
```

Copie o arquivo de exemplo de ambiente:

```powershell
Copy-Item .env.example .env
```

O modo local usa:

```env
DATA_BACKEND=json
LOCAL_DATA_PATH=backend/data/local_db.json
LOCAL_STORAGE_PATH=backend/data/storage
SECRET_KEY=troque-por-uma-chave-secreta-forte
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES_HOURS=8
CLINICAL_ATTACHMENTS_BUCKET=clinical-attachments
ATTACHMENT_SIGNED_URL_EXPIRES_SECONDS=3600
MAX_ATTACHMENT_SIZE_MB=10
```

Supabase continua opcional. Para usar Supabase, altere `DATA_BACKEND=supabase` e
preencha `SUPABASE_URL` e `SUPABASE_KEY`. Use a chave `service_role` apenas no
backend. Ela nao deve ser exposta em frontend.

## Dados locais

O modo padrao grava os dados em:

- `backend/data/local_db.json`
- `backend/data/storage/`

Esses arquivos sao locais e ficam fora do Git. Para reiniciar a demonstracao:

```powershell
.\scripts\reset_local_data.ps1
```

## Supabase opcional

Os scripts do Supabase, caso voce queira usar banco gerenciado, ficam em:

- `supabase/schema.sql`
- `supabase/seed.sql`
- `supabase/migrations/*.sql`

No modo local em JSON, nao e necessario executar SQL.

Se usar Supabase, execute primeiro o `schema.sql` no SQL Editor do Supabase. Depois
execute o `seed.sql` para criar usuarios e dados iniciais de desenvolvimento.

Se o banco ja existir, aplique as migrations em ordem numerica antes de rodar o
seed novamente. Elas adicionam recursos incrementais sem precisar recriar a base.
O schema e a migration `0005` tambem criam o bucket privado
`clinical-attachments` no Supabase Storage para upload de anexos clinicos.

Usuarios criados pelo seed:

| Perfil | E-mail | Senha |
| --- | --- | --- |
| Admin | `admin@hospital.com` | `Admin@123` |
| Medico | `medico@hospital.com` | `Medico@123` |
| Farmacia | `farmacia@hospital.com` | `Farmacia@123` |
| Recepcao | `recepcao@hospital.com` | `Recepcao@123` |

## Como rodar

Backend:

```powershell
.\scripts\run_backend.ps1
```

Depois acesse:

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs
- Healthcheck: http://127.0.0.1:8000/health

Frontend:

```powershell
.\scripts\run_frontend.ps1
```

Depois acesse:

- Frontend: http://127.0.0.1:5173

O frontend le a URL da API por `VITE_API_URL`. Para customizar:

```powershell
cd frontend
Copy-Item .env.example .env
```

Rodar com Docker:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Depois acesse:

- Frontend: http://127.0.0.1:8080
- API: http://127.0.0.1:8000

Para deploy e checklist de producao, consulte `docs/DEPLOY.md`.

## GitHub Pages

O frontend pode ser publicado no GitHub Pages em modo standalone, sem backend e
sem banco externo. Nesse modo, login e dados usam `localStorage` no navegador.

Build local do Pages:

```powershell
cd frontend
npm run build:pages
```

O workflow `.github/workflows/pages.yml` publica automaticamente o conteudo de
`frontend/dist` quando houver push na branch `main`.

No GitHub, ative:

1. `Settings`
2. `Pages`
3. `Source: GitHub Actions`

URL esperada:

```text
https://anntimar.github.io/Sistema-Prontuarios/
```

## Rotas atuais

- `GET /health`
- `POST /register` (admin)
- `POST /login`
- `GET /me`
- `GET /usuarios`
- `GET /usuarios/medicos`
- `POST /usuarios`
- `GET /usuarios/{id_usuario}`
- `PATCH /usuarios/{id_usuario}`
- `GET /pacientes`
- `POST /pacientes`
- `GET /pacientes/{id_paciente}`
- `PATCH /pacientes/{id_paciente}`
- `DELETE /pacientes/{id_paciente}`
- `GET /prontuarios`
- `POST /prontuarios`
- `GET /prontuarios/{id_prontuario}`
- `PATCH /prontuarios/{id_prontuario}`
- `GET /prescricoes`
- `POST /prescricoes`
- `GET /prescricoes/{id_prescricao}`
- `PATCH /prescricoes/{id_prescricao}`
- `PATCH /prescricoes/{id_prescricao}/dispensar`
- `GET /medicamentos`
- `GET /medicamentos/movimentacoes`
- `POST /medicamentos`
- `PATCH /medicamentos/{id_medicamento}`
- `POST /medicamentos/{id_medicamento}/movimentacoes`
- `GET /consultas`
- `POST /consultas`
- `GET /consultas/{id_consulta}`
- `PATCH /consultas/{id_consulta}`
- `GET /anexos`
- `POST /anexos`
- `POST /anexos/upload`
- `DELETE /anexos/{id_anexo}`
- `GET /relatorios/indicadores`
- `GET /relatorios/indicadores/export.csv`
- `GET /auditoria`

Ao criar um prontuario, o backend usa o medico autenticado pelo token. O frontend
nao envia `id_medico`. Quando o prontuario nasce de uma consulta realizada, ele
pode enviar `id_consulta`; o backend valida se a consulta pertence ao mesmo
medico e paciente.

As respostas de prontuarios incluem `paciente_nome` e `medico_nome`. As respostas
de prescricoes incluem contexto do prontuario, como paciente, medico e diagnostico.
As respostas de consultas incluem `paciente_nome` e `medico_nome`. Prescricoes
podem usar texto livre ou itens estruturados vinculados ao estoque, com quantidade
e posologia; itens estruturados exigem medicamento ativo e exibem saldo disponivel
no formulario. O estoque da farmacia controla medicamentos, entrada/saida e alerta
de baixo estoque. Os anexos clinicos podem ser vinculados ao paciente e, opcionalmente, a um prontuario.
Anexos enviados por upload ficam em bucket privado e recebem `download_url`
assinado na resposta da API. Os relatorios gerenciais incluem totais e graficos
de consultas por status e por dia agendado.

Filtros disponiveis:

- `GET /pacientes?search=&cpf=`
- `GET /prontuarios?id_paciente=&created_from=&created_to=`
- `GET /prescricoes?status=`
- `GET /medicamentos?search=&ativo=&baixo_estoque=`
- `GET /medicamentos/movimentacoes?id_medicamento=&tipo=`
- `GET /consultas?id_paciente=&id_medico=&status=&scheduled_from=&scheduled_to=`
- `GET /anexos?id_paciente=&id_prontuario=&tipo=`
- `GET /usuarios?search=&role=&ativo=`
- `GET /relatorios/indicadores?created_from=&created_to=`
- `GET /relatorios/indicadores/export.csv?created_from=&created_to=`
- `GET /auditoria?action=&resource_type=&actor_email=&created_from=&created_to=`

## Testes

Rodar todos os checks:

```powershell
.\scripts\check_project.ps1
```

Backend manual:

```powershell
python -m unittest discover -s tests
```

Frontend:

```powershell
cd frontend
npm run build
npm audit
```

Guia de operacao e demonstracao:

- `docs/OPERACAO.md`
- `docs/DEPLOY.md`

Smoke test da API com backend rodando:

```powershell
python scripts/smoke_api.py
```

Para usar outro usuario no smoke test:

```powershell
$env:SMOKE_EMAIL="admin@hospital.com"
$env:SMOKE_PASSWORD="Admin@123"
python scripts/smoke_api.py
```

## Checklist ponta a ponta

1. Rodar `.\scripts\setup_dev.ps1`.
2. Subir o backend com `.\scripts\run_backend.ps1`.
3. Abrir `http://127.0.0.1:8000/health`.
4. Rodar `python scripts/smoke_api.py`.
5. Subir o frontend com `.\scripts\run_frontend.ps1`.
6. Entrar em `http://127.0.0.1:5173` ou na porta indicada pelo Vite usando `medico@hospital.com` e `Medico@123`.

## Funcionalidades do frontend

- Login com JWT.
- Modo GitHub Pages standalone, com login e dados no `localStorage`.
- Painel com contadores principais.
- Relatorios gerenciais para `admin`, com periodo, totais, prescricoes, consultas e diagnosticos recorrentes.
- Exportacao CSV dos relatorios gerenciais.
- Impressao dos relatorios gerenciais para PDF pelo navegador.
- Auditoria operacional para `admin`, com filtros por usuario, acao, recurso e periodo.
- Gestao de usuarios e perfis para `admin`.
- Busca e listagem de pacientes por nome e CPF.
- Painel de detalhe do paciente com cadastro, historico clinico, prescricoes e anexos clinicos vinculados.
- Registro de anexos clinicos por upload privado ou URL externa, com tipo, observacoes e vinculo opcional ao prontuario.
- Impressao da ficha do paciente em formato limpo para salvar como PDF.
- Cadastro e edicao de pacientes para `admin` e `recepcao`.
- Remocao de pacientes para `admin`.
- Cadastro e listagem de prontuarios para `medico`.
- Criacao de prontuario a partir de consulta realizada.
- Listagem de prontuarios com filtros por paciente e periodo.
- Historico clinico com nomes de paciente e medico.
- Criacao, edicao e cancelamento de prescricoes pendentes para `medico`.
- Prescricao estruturada por medicamento ativo do estoque, quantidade, saldo disponivel e posologia, mantendo texto livre como compatibilidade.
- Filtro de prescricoes por status.
- Fila da farmacia com paciente, diagnostico, medico e medicamentos.
- Dispensacao de prescricoes pendentes para `farmaceutico`.
- Controle de estoque da farmacia, com cadastro de medicamentos, entrada/saida, historico de movimentacoes e alerta de baixo estoque.
- Agenda de consultas para `admin`, `recepcao` e `medico`.
- Agendamento e reagendamento de consultas para `admin` e `recepcao`.
- Atualizacao de status de consultas para `admin`, `recepcao` e `medico`.
- Filtros de agenda por paciente, medico, status e periodo.

## Estrutura do backend

```text
backend/
  core/        Configuracao, seguranca e tratamento de erros
  database/    Cliente JSON local e adaptador Supabase opcional
  routes/      Rotas HTTP
  schemas/     Modelos Pydantic e validacoes
  services/    Regras de acesso a dados
  main.py      Ponto de entrada da aplicacao
supabase/
  schema.sql   Estrutura opcional do banco Supabase
  seed.sql     Dados iniciais opcionais para Supabase
  migrations/  Atualizacoes incrementais opcionais
tests/
  test_api_contract.py
scripts/
  smoke_api.py
frontend/
  src/         Aplicacao React
  package.json
```

## Perfis suportados

- `admin`
- `medico`
- `farmaceutico`
- `recepcao`

## Permissoes atuais

| Funcionalidade | Admin | Medico | Farmacia | Recepcao |
| --- | --- | --- | --- | --- |
| Ver relatorios | Sim | Nao | Nao | Nao |
| Ver auditoria | Sim | Nao | Nao | Nao |
| Gerenciar usuarios | Sim | Nao | Nao | Nao |
| Ver pacientes | Sim | Sim | Nao | Sim |
| Criar/editar pacientes | Sim | Nao | Nao | Sim |
| Remover pacientes | Sim | Nao | Nao | Nao |
| Ver prontuarios | Sim | Apenas proprios | Nao | Sim |
| Criar/editar prontuarios | Nao | Apenas proprios | Nao | Nao |
| Ver prescricoes | Sim | Apenas proprias | Sim | Nao |
| Criar/editar prescricoes | Nao | Apenas proprias pendentes | Nao | Nao |
| Dispensar prescricoes | Nao | Nao | Sim | Nao |
| Ver estoque da farmacia | Sim | Sim | Sim | Nao |
| Gerenciar estoque da farmacia | Sim | Nao | Sim | Nao |
| Ver agenda | Sim | Apenas proprias | Nao | Sim |
| Agendar/reagendar consultas | Sim | Nao | Nao | Sim |
| Atualizar status de consulta | Sim | Apenas proprias | Nao | Sim |
| Ver/criar anexos clinicos | Sim | Sim | Nao | Sim |
| Remover anexos clinicos | Sim | Nao | Nao | Nao |
