# Deploy do Sistema-Prontuarios

Este guia cobre uma entrega simples e profissional usando FastAPI como backend,
React estatico servido por Nginx e banco local JSON por padrao. Supabase continua
disponivel como backend opcional.

## Variaveis obrigatorias

Backend local:

- `DATA_BACKEND=json`
- `SECRET_KEY` forte e exclusiva do ambiente
- `FRONTEND_ORIGINS` com as URLs publicas do frontend separadas por virgula

Backend Supabase:

- `DATA_BACKEND=supabase`
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

2. Para rodar simples, mantenha `DATA_BACKEND=json`.

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

## GitHub Pages standalone

Este e o caminho mais simples para demonstracao publica sem backend.

1. Garanta que o GitHub Pages do repositorio esteja configurado para GitHub Actions:
   `Settings > Pages > Source > GitHub Actions`.
2. Faça push na branch `main`.
3. O workflow `.github/workflows/pages.yml` executa `npm run build:pages`.
4. O app publicado usa `VITE_STANDALONE=true`, ou seja, login e dados ficam no
   `localStorage` do navegador de cada visitante.

URL esperada:

```text
https://lucascaldass.github.io/Sistema-Prontuarios/
```

Limites desse modo:

- Dados ficam apenas no navegador de quem acessa.
- Cada visitante tem sua propria base de demonstracao.
- Nao ha backend compartilhado nem banco central.

## Deploy em producao

Uma separacao comum:

- Backend em Render, Railway, Fly.io, VPS ou outro host que rode container.
- Frontend em Nginx container, Vercel, Netlify, Cloudflare Pages ou outro host
  estatico.
- Banco local JSON para demonstracao simples ou Supabase para uma entrega com banco gerenciado.

Passos recomendados:

1. Configurar `SECRET_KEY` forte no backend.
2. Configurar `FRONTEND_ORIGINS` com o dominio HTTPS do frontend.
3. Gerar o build do frontend com `VITE_API_URL` apontando para o dominio HTTPS da API.
4. Validar `/health`, `/docs`, login e smoke test.
5. Se usar Supabase, aplicar `supabase/schema.sql`, migrations e `seed.sql`.
6. Se usar Supabase, configurar `SUPABASE_KEY` somente no backend, nunca no frontend.

## Checklist antes de apresentar

- `.\scripts\check_project.ps1` passando.
- `npm audit` sem vulnerabilidades conhecidas.
- `/health` retornando `supabase_configured: true` e `secret_key_configured: true`.
- Login funcionando para `admin`, `medico`, `farmaceutico` e `recepcao`.
- Upload de anexo testado no storage local ou no bucket privado `clinical-attachments`.
- Prescricao estruturada testada com baixa de estoque.
- `FRONTEND_ORIGINS` sem `*` em producao.
- `.env` fora do Git.

## Rollback simples

- Backend: voltar a imagem/container anterior no provedor.
- Frontend: voltar o ultimo build estatico publicado.
- Banco: manter backup/export antes de aplicar migrations em producao.

Evite rodar seed em producao, porque ele cria usuarios e dados de demonstracao.
