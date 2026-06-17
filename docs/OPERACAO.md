# Operacao do Sistema

Este guia resume o fluxo para preparar, rodar, validar e demonstrar o projeto.

## Preparar ambiente

No PowerShell, a partir da raiz do projeto:

```powershell
.\scripts\setup_dev.ps1
```

Depois crie o arquivo `.env`:

```powershell
Copy-Item .env.example .env
```

Por padrao o sistema usa `DATA_BACKEND=json`, criando uma base local em
`backend/data/local_db.json`. Nao precisa de Supabase para demonstrar.

## Preparar banco

No modo padrao JSON, a base nasce automaticamente a partir de
`backend/data/local_seed.json`.

Para restaurar a base de demonstracao:

```powershell
.\scripts\reset_local_data.ps1
```

Se optar por Supabase, configure `DATA_BACKEND=supabase` no `.env` e execute no
SQL Editor do Supabase:

1. `supabase/schema.sql`
2. `supabase/seed.sql`

Para atualizar um banco Supabase que ja existe, execute os arquivos de
`supabase/migrations` em ordem numerica antes de reaplicar o seed.

## Rodar localmente

Terminal 1:

```powershell
.\scripts\run_backend.ps1
```

Terminal 2:

```powershell
.\scripts\run_frontend.ps1
```

Acesse:

- Frontend: http://127.0.0.1:5173
- Swagger: http://127.0.0.1:8000/docs
- Healthcheck: http://127.0.0.1:8000/health

## Validar qualidade

```powershell
.\scripts\check_project.ps1
```

Se o `npm audit` nao puder acessar a internet no ambiente atual:

```powershell
.\scripts\check_project.ps1 -SkipAudit
```

## Roteiro rapido de demonstracao

1. Entrar como `admin@hospital.com` e mostrar painel, usuarios, relatorios e auditoria.
2. No relatorio, filtrar um periodo, conferir consultas por status/dia, exportar o CSV e testar `Imprimir relatorio`.
3. Criar ou editar um paciente pela recepcao/admin.
4. Abrir o detalhe do paciente e usar `Imprimir ficha` para gerar PDF pelo navegador.
5. Ainda como recepcao/admin, abrir Agenda e criar uma consulta para o medico.
6. Entrar como `medico@hospital.com`, abrir Agenda e marcar a consulta como realizada.
7. Usar `Gerar prontuario` na consulta realizada para abrir o formulario ja vinculado ao paciente.
8. No detalhe do paciente, enviar um anexo clinico em PDF ou imagem e vincular ao prontuario.
9. Criar uma prescricao para o prontuario usando um item estruturado ativo do estoque e conferir o saldo disponivel.
10. Entrar como `farmacia@hospital.com`, conferir o estoque, filtrar prescricoes pendentes e dispensar.
11. Ver a baixa de estoque, o historico de movimentacoes e o alerta de baixo estoque quando a quantidade estiver no minimo.
12. Voltar ao admin e mostrar relatorios atualizados e eventos registrados em Auditoria.
