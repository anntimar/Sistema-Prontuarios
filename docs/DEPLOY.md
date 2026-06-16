# Deploy do Sistema-Prontuarios

Este guia cobre uma entrega simples e profissional usando Supabase como banco,
FastAPI como backend e React estatico servido por Nginx.

## Variaveis obrigatorias

Backend:

- `SUPABASE_URL`
- `SUPABASE_KEY` com chave `service_role`
- `SECRET_KEY` forte e exclusiva do ambiente
- `FRONTEND_ORIGINS` com as URLs publicas do frontend separadas por virgula

Frontend:

- `VITE_API_URL` com a URL publica da API, por exemplo `https://api.seudominio.com`

O frontend recebe `VITE_API_URL` em tempo de build. Se a URL da API mudar em
producao, gere uma nova imagem/build do frontend.

## Rodar com Docker local

1. Copie o exemplo de ambiente:

```powershell
Copy-Item .env.example .env
```

2. Preencha `.env` com as credenciais reais do Supabase.

3. Para o ambiente local com Docker, ajuste:

```env
DOCKER_FRONTEND_ORIGINS=http://127.0.0.1:8080,http://localhost:8080
VITE_API_URL=http://127.0.0.1:8000
```

4. Suba os containers:

```powershell
docker compose up --build
```

5. Acesse:

- Frontend: http://127.0.0.1:8080
- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

6. Rode o smoke test contra a API em container:

```powershell
$env:API_URL="http://127.0.0.1:8000"
.\.venv\Scripts\python.exe scripts\smoke_api.py
```

## Deploy em producao

Uma separacao comum:

- Backend em Render, Railway, Fly.io, VPS ou outro host que rode container.
- Frontend em Nginx container, Vercel, Netlify, Cloudflare Pages ou outro host
  estatico.
- Banco, Storage e autenticacao de dados no Supabase.

Passos recomendados:

1. Aplicar `supabase/schema.sql` em um projeto Supabase novo.
2. Aplicar as migrations de `supabase/migrations` em ordem numerica quando estiver atualizando uma base existente.
3. Rodar `supabase/seed.sql` apenas em ambiente de demonstracao/desenvolvimento.
4. Configurar `SECRET_KEY` forte no backend.
5. Configurar `SUPABASE_KEY` somente no backend, nunca no frontend.
6. Configurar `FRONTEND_ORIGINS` com o dominio HTTPS do frontend.
7. Gerar o build do frontend com `VITE_API_URL` apontando para o dominio HTTPS da API.
8. Validar `/health`, `/docs`, login e smoke test.

## Checklist antes de apresentar

- `.\scripts\check_project.ps1` passando.
- `npm audit` sem vulnerabilidades conhecidas.
- `/health` retornando `supabase_configured: true` e `secret_key_configured: true`.
- Login funcionando para `admin`, `medico`, `farmaceutico` e `recepcao`.
- Upload de anexo testado com bucket privado `clinical-attachments`.
- Prescricao estruturada testada com baixa de estoque.
- `FRONTEND_ORIGINS` sem `*` em producao.
- `.env` fora do Git.

## Rollback simples

- Backend: voltar a imagem/container anterior no provedor.
- Frontend: voltar o ultimo build estatico publicado.
- Banco: manter backup/export antes de aplicar migrations em producao.

Evite rodar seed em producao, porque ele cria usuarios e dados de demonstracao.
