# Modelagem BPMN - Permissoes e processos do sistema

Este documento foi feito para ajudar a desenhar os BPMN do Sistema de
Prontuarios. A ideia e ser direto: quem faz, o que pode fazer, onde entra o
gateway, quais sao as condicoes e como o processo termina.

## 1. Como ler este documento

Para cada processo, use esta estrutura no BPMN:

- Inicio: evento inicial do processo.
- Raias: participantes do processo.
- Tarefas: atividades feitas por usuario ou pelo sistema.
- Gateway: ponto de decisao, normalmente uma pergunta com resposta Sim/Nao.
- Condicoes: regras que precisam ser verdadeiras para o fluxo continuar.
- Fim: resultado final do processo.

Na ferramenta BPMN:

- Use retangulo para tarefa.
- Use losango para gateway/decisao.
- Use circulo para inicio e fim.
- Use raias para separar Admin, Recepcao, Medico, Farmacia e Sistema.

## 2. Perfis e permissoes

O sistema possui quatro perfis principais:

- Admin
- Recepcao
- Medico
- Farmacia

Tambem existe a raia "Sistema de Prontuarios", que representa validacoes,
salvamentos, atualizacoes de status, auditoria e relatorios.

## 3. O que cada usuario pode fazer

### 3.1 Admin

O Admin e o usuario com maior permissao administrativa.

Pode fazer:

- Entrar no sistema.
- Ver o painel inicial.
- Gerenciar usuarios.
- Criar usuarios.
- Editar usuarios.
- Ativar ou desativar usuarios.
- Consultar pacientes.
- Cadastrar pacientes.
- Editar pacientes.
- Remover pacientes.
- Consultar agenda.
- Criar e editar consultas.
- Consultar prontuarios.
- Consultar prescricoes.
- Consultar medicamentos.
- Gerenciar estoque de medicamentos.
- Adicionar anexos clinicos.
- Excluir anexos clinicos.
- Ver relatorios.
- Exportar relatorios.
- Imprimir relatorios.
- Consultar auditoria.
- Resetar a base de demonstracao.

Nao deve fazer:

- Registrar atendimento clinico como medico.
- Criar prontuario clinico no lugar do medico.
- Criar prescricao medica no lugar do medico.
- Dispensar medicamento no lugar da farmacia.

Resumo para BPMN:

- Use Admin em processos administrativos.
- Use Admin em relatorios e auditoria.
- Use Admin como apoio em cadastros e estoque.
- Nao use Admin como responsavel principal por atendimento medico.

### 3.2 Recepcao

A Recepcao cuida da entrada do paciente e da organizacao da agenda.

Pode fazer:

- Entrar no sistema.
- Ver o painel inicial.
- Cadastrar pacientes.
- Editar dados de pacientes.
- Consultar pacientes.
- Agendar consultas.
- Editar consultas.
- Cancelar consultas.
- Consultar agenda.
- Consultar prontuarios ja existentes.
- Adicionar anexos clinicos ao paciente.
- Consultar anexos.

Nao pode fazer:

- Criar usuarios.
- Editar usuarios.
- Criar prontuario clinico.
- Criar prescricao.
- Dispensar medicamento.
- Gerenciar estoque.
- Ver relatorios gerenciais.
- Consultar auditoria.
- Excluir anexos clinicos.

Resumo para BPMN:

- Use Recepcao no inicio do atendimento.
- Use Recepcao para cadastro de paciente.
- Use Recepcao para agendamento.
- Use Recepcao para anexar documentos iniciais.

### 3.3 Medico

O Medico realiza o atendimento clinico.

Pode fazer:

- Entrar no sistema.
- Ver o painel inicial.
- Consultar pacientes.
- Consultar historico do paciente.
- Consultar agenda.
- Atualizar status da consulta.
- Marcar consulta como realizada.
- Criar prontuario.
- Consultar prontuarios.
- Criar prescricoes.
- Editar prescricoes pendentes.
- Cancelar prescricoes pendentes.
- Consultar medicamentos.
- Consultar prescricoes.
- Adicionar anexos clinicos.
- Consultar anexos clinicos.

Nao pode fazer:

- Cadastrar usuarios.
- Editar usuarios.
- Cadastrar ou editar paciente.
- Remover paciente.
- Gerenciar estoque.
- Dispensar medicamentos.
- Ver relatorios gerenciais.
- Consultar auditoria.
- Excluir anexos clinicos.

Resumo para BPMN:

- Use Medico no atendimento.
- Use Medico para prontuario.
- Use Medico para prescricao.
- Use Medico para marcar consulta como realizada.

### 3.4 Farmacia

A Farmacia controla medicamentos e dispensacao.

Pode fazer:

- Entrar no sistema.
- Ver o painel inicial.
- Consultar prescricoes.
- Ver prescricoes pendentes.
- Dispensar prescricoes.
- Consultar medicamentos.
- Cadastrar medicamentos.
- Editar medicamentos.
- Fazer entrada de estoque.
- Fazer saida de estoque.
- Consultar movimentacoes de estoque.
- Ver alerta de baixo estoque.

Nao pode fazer:

- Cadastrar pacientes.
- Editar pacientes.
- Consultar prontuario completo como modulo principal.
- Criar prontuario.
- Criar prescricao.
- Agendar consultas.
- Gerenciar usuarios.
- Ver relatorios gerenciais.
- Consultar auditoria.
- Adicionar ou excluir anexos clinicos.

Resumo para BPMN:

- Use Farmacia quando existir prescricao pendente.
- Use Farmacia para confirmar dispensacao.
- Use Farmacia para controlar estoque.

## 4. Tabela simples de permissoes

| Funcionalidade | Admin | Recepcao | Medico | Farmacia |
| --- | --- | --- | --- | --- |
| Login | Sim | Sim | Sim | Sim |
| Painel | Sim | Sim | Sim | Sim |
| Cadastrar paciente | Sim | Sim | Nao | Nao |
| Editar paciente | Sim | Sim | Nao | Nao |
| Remover paciente | Sim | Nao | Nao | Nao |
| Consultar paciente | Sim | Sim | Sim | Nao |
| Agendar consulta | Sim | Sim | Nao | Nao |
| Atualizar status da consulta | Sim | Sim | Sim | Nao |
| Criar prontuario | Nao | Nao | Sim | Nao |
| Consultar prontuario | Sim | Sim | Sim | Nao |
| Criar prescricao | Nao | Nao | Sim | Nao |
| Editar/cancelar prescricao pendente | Nao | Nao | Sim | Nao |
| Consultar prescricao | Sim | Nao | Sim | Sim |
| Dispensar prescricao | Nao | Nao | Nao | Sim |
| Gerenciar medicamentos | Sim | Nao | Nao | Sim |
| Consultar medicamentos | Sim | Nao | Sim | Sim |
| Adicionar anexo | Sim | Sim | Sim | Nao |
| Excluir anexo | Sim | Nao | Nao | Nao |
| Gerenciar usuarios | Sim | Nao | Nao | Nao |
| Ver relatorios | Sim | Nao | Nao | Nao |
| Ver auditoria | Sim | Nao | Nao | Nao |

## 5. Processos para modelar em BPMN

Os principais processos sao:

- P01 - Login e controle de acesso.
- P02 - Gestao de usuarios.
- P03 - Cadastro de paciente.
- P04 - Agendamento de consulta.
- P05 - Atendimento medico e prontuario.
- P06 - Prescricao medica.
- P07 - Dispensacao de medicamento.
- P08 - Controle de estoque.
- P09 - Anexos clinicos.
- P10 - Relatorios e auditoria.
- P11 - Fluxo completo de atendimento.

## 6. P01 - Login e controle de acesso

Objetivo:

Permitir que apenas usuarios autorizados entrem no sistema.

Raias:

- Usuario
- Sistema de Prontuarios

Inicio:

Usuario acessa a tela de login.

Fluxo:

1. Usuario informa e-mail.
2. Usuario informa senha.
3. Usuario clica em Entrar.
4. Sistema recebe os dados.
5. Sistema procura usuario pelo e-mail.

Gateway 1:

Usuario existe?

- Se sim: continuar.
- Se nao: mostrar mensagem de login invalido e encerrar processo.

6. Sistema verifica se o usuario esta ativo.

Gateway 2:

Usuario esta ativo?

- Se sim: continuar.
- Se nao: bloquear acesso e encerrar processo.

7. Sistema confere a senha.

Gateway 3:

Senha esta correta?

- Se sim: continuar.
- Se nao: mostrar mensagem de login invalido e encerrar processo.

8. Sistema identifica o perfil do usuario.
9. Sistema libera apenas os menus permitidos para o perfil.
10. Sistema registra acesso.

Condicoes:

- E-mail deve estar cadastrado.
- Senha deve estar correta.
- Usuario deve estar ativo.
- Perfil deve possuir permissao para acessar os modulos.

Fim:

Usuario entra no sistema com permissoes do seu perfil.

## 7. P02 - Gestao de usuarios

Objetivo:

Permitir que o Admin cadastre e mantenha usuarios do sistema.

Raias:

- Admin
- Sistema de Prontuarios

Inicio:

Admin precisa criar ou alterar um acesso.

Fluxo:

1. Admin entra no sistema.
2. Admin acessa o modulo Usuarios.
3. Sistema lista usuarios cadastrados.
4. Admin escolhe criar novo usuario ou editar usuario existente.

Gateway 1:

Acao e criar novo usuario?

- Se sim: abrir formulario vazio.
- Se nao: carregar dados do usuario selecionado.

5. Admin informa nome.
6. Admin informa e-mail.
7. Admin escolhe perfil: admin, medico, recepcao ou farmaceutico.
8. Admin informa senha, quando necessario.
9. Admin define se usuario esta ativo.
10. Sistema valida campos obrigatorios.

Gateway 2:

Dados obrigatorios foram preenchidos?

- Se sim: continuar.
- Se nao: mostrar erro e voltar ao formulario.

11. Sistema verifica se e-mail ja esta em uso.

Gateway 3:

E-mail ja existe?

- Se sim: bloquear cadastro ou alteracao.
- Se nao: salvar usuario.

12. Sistema registra auditoria.
13. Sistema atualiza lista de usuarios.

Condicoes:

- Apenas Admin pode gerenciar usuarios.
- E-mail deve ser unico.
- Perfil deve ser valido.
- Usuario inativo nao pode fazer login.

Fim:

Usuario criado ou atualizado.

## 8. P03 - Cadastro de paciente

Objetivo:

Cadastrar um paciente para permitir agendamento, prontuario e anexos.

Raias:

- Recepcao
- Sistema de Prontuarios

Inicio:

Paciente chega ou solicita atendimento.

Fluxo:

1. Recepcao acessa o modulo Pacientes.
2. Recepcao pesquisa paciente por nome ou CPF.
3. Sistema procura paciente cadastrado.

Gateway 1:

Paciente ja existe?

- Se sim: sistema mostra cadastro existente.
- Se nao: recepcao inicia novo cadastro.

4. Recepcao informa nome.
5. Recepcao informa CPF.
6. Recepcao informa data de nascimento.
7. Recepcao informa telefone.
8. Sistema valida dados obrigatorios.

Gateway 2:

Dados estao completos?

- Se sim: salvar paciente.
- Se nao: mostrar erro e voltar ao formulario.

9. Sistema grava cadastro.
10. Sistema registra auditoria.
11. Sistema deixa paciente disponivel para agenda e atendimento.

Condicoes:

- Nome, CPF, data de nascimento e telefone devem ser preenchidos.
- Recepcao e Admin podem cadastrar ou editar.
- Medico apenas consulta.
- Apenas Admin remove paciente.

Fim:

Paciente cadastrado ou atualizado.

## 9. P04 - Agendamento de consulta

Objetivo:

Agendar consulta entre paciente e medico.

Raias:

- Recepcao
- Sistema de Prontuarios

Inicio:

Paciente solicita uma consulta.

Fluxo:

1. Recepcao acessa Agenda.
2. Recepcao pesquisa paciente.

Gateway 1:

Paciente esta cadastrado?

- Se sim: continuar.
- Se nao: voltar ao processo P03 - Cadastro de paciente.

3. Recepcao seleciona medico.
4. Recepcao informa data e horario.
5. Recepcao informa observacoes, se houver.
6. Sistema valida dados.

Gateway 2:

Paciente, medico e data foram informados?

- Se sim: continuar.
- Se nao: mostrar erro e voltar ao formulario.

7. Sistema cria consulta com status Agendada.
8. Sistema registra auditoria.
9. Sistema mostra consulta na agenda.

Condicoes:

- Paciente deve existir.
- Medico deve existir e estar ativo.
- Consulta nova inicia como Agendada.
- Status possiveis: Agendada, Realizada ou Cancelada.

Fim:

Consulta fica agendada.

## 10. P05 - Atendimento medico e prontuario

Objetivo:

Registrar o atendimento clinico realizado pelo medico.

Raias:

- Medico
- Sistema de Prontuarios

Inicio:

Medico vai atender paciente.

Fluxo:

1. Medico entra no sistema.
2. Medico acessa Agenda ou Pacientes.
3. Medico seleciona paciente.
4. Sistema mostra dados do paciente.
5. Sistema mostra historico clinico.
6. Medico realiza atendimento.
7. Medico registra anamnese.
8. Medico registra diagnostico.
9. Medico registra observacoes.

Gateway 1:

Atendimento veio de consulta agendada?

- Se sim: vincular prontuario a consulta.
- Se nao: criar prontuario sem consulta vinculada.

10. Sistema valida dados do prontuario.

Gateway 2:

Dados clinicos foram preenchidos?

- Se sim: salvar prontuario.
- Se nao: mostrar erro e voltar ao formulario.

11. Sistema salva prontuario.
12. Sistema registra auditoria.

Gateway 3:

Medico precisa gerar prescricao?

- Se sim: seguir para P06 - Prescricao medica.
- Se nao: finalizar atendimento.

Condicoes:

- Apenas Medico cria prontuario.
- Paciente deve estar cadastrado.
- Prontuario deve ter paciente e medico.
- Prontuario deve conter anamnese, diagnostico e observacoes.

Fim:

Prontuario fica registrado no historico do paciente.

## 11. P06 - Prescricao medica

Objetivo:

Registrar medicamentos prescritos pelo medico apos atendimento.

Raias:

- Medico
- Sistema de Prontuarios

Inicio:

Medico decide prescrever medicamento.

Fluxo:

1. Medico acessa Prescricoes.
2. Medico seleciona prontuario do paciente.

Gateway 1:

Prontuario existe?

- Se sim: continuar.
- Se nao: voltar ao processo P05 - Atendimento e prontuario.

3. Sistema mostra paciente e diagnostico.
4. Medico seleciona medicamento.
5. Medico informa quantidade.
6. Medico informa posologia.
7. Medico adiciona item na prescricao.

Gateway 2:

Existe pelo menos um medicamento na prescricao?

- Se sim: continuar.
- Se nao: pedir ao medico para adicionar medicamento.

8. Sistema valida se medicamento esta ativo.

Gateway 3:

Medicamento esta ativo?

- Se sim: continuar.
- Se nao: bloquear item e pedir outro medicamento.

9. Sistema salva prescricao com status Pendente.
10. Sistema registra auditoria.
11. Sistema envia prescricao para fila da farmacia.

Condicoes:

- Apenas Medico cria prescricao.
- Prescricao deve estar vinculada a prontuario.
- Prescricao nova inicia como Pendente.
- Prescricao Pendente pode ser editada ou cancelada pelo medico.
- Prescricao Entregue nao pode ser editada.
- Prescricao Cancelada nao vai para farmacia.

Fim:

Prescricao fica pendente para dispensacao.

## 12. P07 - Dispensacao de medicamento

Objetivo:

Permitir que a Farmacia entregue medicamentos prescritos e atualize o estoque.

Raias:

- Farmacia
- Sistema de Prontuarios

Inicio:

Farmacia recebe ou consulta uma prescricao pendente.

Fluxo:

1. Farmacia acessa Prescricoes.
2. Sistema lista prescricoes pendentes.
3. Farmacia seleciona uma prescricao.
4. Sistema mostra paciente, medico, diagnostico e medicamentos.
5. Sistema verifica status da prescricao.

Gateway 1:

Prescricao esta Pendente?

- Se sim: continuar.
- Se nao: bloquear dispensacao.

6. Sistema verifica saldo de cada medicamento.

Gateway 2:

Existe estoque suficiente?

- Se sim: continuar.
- Se nao: bloquear dispensacao e informar falta de estoque.

7. Farmacia confirma entrega.
8. Sistema baixa quantidade do estoque.
9. Sistema cria movimentacao de estoque do tipo Saida.
10. Sistema altera prescricao para Entregue.
11. Sistema registra data/hora da dispensacao.
12. Sistema registra auditoria.

Condicoes:

- Apenas Farmacia dispensa medicamentos.
- Prescricao deve estar Pendente.
- Estoque deve ser suficiente.
- Sistema nao deve permitir saldo negativo.
- Prescricao Entregue nao pode ser dispensada de novo.

Fim:

Medicamento entregue, prescricao marcada como Entregue e estoque atualizado.

## 13. P08 - Controle de estoque

Objetivo:

Controlar cadastro, entrada e saida de medicamentos.

Raias:

- Farmacia
- Sistema de Prontuarios

Inicio:

Farmacia precisa cadastrar medicamento ou atualizar estoque.

Fluxo:

1. Farmacia acessa Medicamentos.
2. Sistema lista medicamentos cadastrados.
3. Farmacia escolhe cadastrar, editar ou movimentar estoque.

Gateway 1:

Acao e cadastrar/editar medicamento?

- Se sim: preencher dados do medicamento.
- Se nao: seguir para movimentacao de estoque.

4. Farmacia informa nome do medicamento.
5. Farmacia informa apresentacao.
6. Farmacia informa quantidade.
7. Farmacia informa estoque minimo.
8. Farmacia define se medicamento esta ativo.
9. Sistema valida dados.

Gateway 2:

Dados do medicamento estao completos?

- Se sim: salvar medicamento.
- Se nao: mostrar erro.

10. Para movimentacao, farmacia escolhe Entrada ou Saida.
11. Farmacia informa quantidade movimentada.
12. Sistema calcula saldo anterior e saldo atual.

Gateway 3:

Movimentacao e Saida?

- Se sim: verificar saldo disponivel.
- Se nao: registrar entrada.

Gateway 4:

Saldo e suficiente para saida?

- Se sim: registrar saida.
- Se nao: bloquear movimentacao.

13. Sistema salva movimentacao.
14. Sistema verifica se estoque ficou baixo.

Gateway 5:

Quantidade atual e menor ou igual ao estoque minimo?

- Se sim: sinalizar baixo estoque.
- Se nao: manter status normal.

15. Sistema registra auditoria.

Condicoes:

- Farmacia e Admin podem gerenciar medicamentos.
- Medicamento deve ter nome, apresentacao, quantidade e estoque minimo.
- Saida nao pode deixar estoque negativo.
- Medicamento inativo nao deve ser usado em novas prescricoes.

Fim:

Medicamento cadastrado/atualizado ou estoque movimentado.

## 14. P09 - Anexos clinicos

Objetivo:

Adicionar documentos ao historico do paciente.

Raias:

- Recepcao
- Medico
- Sistema de Prontuarios

Inicio:

Usuario precisa anexar exame, laudo, imagem ou outro documento.

Fluxo:

1. Usuario acessa detalhe do paciente.
2. Usuario escolhe adicionar anexo.
3. Usuario informa tipo do anexo.
4. Usuario informa titulo.
5. Usuario informa observacoes.
6. Usuario envia arquivo ou informa link.

Gateway 1:

Arquivo ou link foi informado?

- Se sim: continuar.
- Se nao: mostrar erro.

7. Usuario escolhe se vai vincular a um prontuario.

Gateway 2:

Anexo sera vinculado a prontuario?

- Se sim: selecionar prontuario do paciente.
- Se nao: salvar apenas no paciente.

8. Sistema valida dados.
9. Sistema salva anexo.
10. Sistema registra responsavel.
11. Sistema registra auditoria.

Condicoes:

- Anexo deve pertencer a um paciente.
- Anexo pode ou nao estar vinculado a prontuario.
- Recepcao, Medico e Admin podem adicionar anexos.
- Apenas Admin pode excluir anexos.

Fim:

Anexo fica disponivel no historico do paciente.

## 15. P10 - Relatorios e auditoria

Objetivo:

Permitir que o Admin acompanhe indicadores e veja historico de acoes.

Raias:

- Admin
- Sistema de Prontuarios

Inicio:

Admin precisa analisar informacoes do sistema.

Fluxo de relatorios:

1. Admin acessa Relatorios.
2. Admin informa periodo.
3. Sistema busca dados do periodo.
4. Sistema calcula totais.
5. Sistema agrupa consultas por status.
6. Sistema agrupa prescricoes por status.
7. Sistema mostra graficos e indicadores.

Gateway 1:

Admin deseja exportar?

- Se sim: sistema gera CSV.
- Se nao: manter visualizacao.

Gateway 2:

Admin deseja imprimir?

- Se sim: sistema abre impressao do navegador.
- Se nao: finalizar consulta.

Fluxo de auditoria:

1. Admin acessa Auditoria.
2. Admin informa filtros.
3. Sistema pesquisa registros.

Gateway 3:

Existem registros para os filtros?

- Se sim: mostrar logs.
- Se nao: mostrar mensagem de nenhum resultado.

Condicoes:

- Apenas Admin acessa relatorios.
- Apenas Admin acessa auditoria.
- Relatorio deve respeitar periodo escolhido.
- Auditoria deve mostrar usuario, acao, recurso e data/hora.

Fim:

Admin visualiza indicadores, exporta relatorio ou consulta auditoria.

## 16. P11 - Fluxo completo de atendimento

Este e o melhor processo para desenhar como BPMN principal do trabalho.

Objetivo:

Mostrar o caminho completo desde a chegada do paciente ate a dispensacao do medicamento.

Raias:

- Recepcao
- Medico
- Farmacia
- Sistema de Prontuarios

Inicio:

Paciente solicita atendimento.

Fluxo:

1. Recepcao pesquisa paciente.

Gateway 1:

Paciente ja esta cadastrado?

- Se sim: seguir para agendamento.
- Se nao: cadastrar paciente.

2. Recepcao agenda consulta.
3. Sistema cria consulta como Agendada.
4. Medico acessa agenda.
5. Medico realiza atendimento.
6. Medico marca consulta como Realizada.
7. Medico registra prontuario.

Gateway 2:

Atendimento precisa de prescricao?

- Se sim: medico cria prescricao.
- Se nao: finalizar atendimento.

8. Sistema cria prescricao como Pendente.
9. Farmacia acessa prescricoes pendentes.
10. Farmacia seleciona prescricao.
11. Sistema verifica estoque.

Gateway 3:

Existe estoque suficiente?

- Se sim: farmacia dispensa medicamento.
- Se nao: farmacia nao dispensa e precisa regularizar estoque.

12. Sistema baixa estoque.
13. Sistema marca prescricao como Entregue.
14. Sistema registra auditoria.
15. Sistema atualiza relatorios.

Condicoes:

- Paciente precisa estar cadastrado.
- Consulta precisa ter paciente, medico e data.
- Apenas medico cria prontuario.
- Apenas medico cria prescricao.
- Apenas farmacia dispensa.
- Estoque nao pode ficar negativo.

Fim:

Atendimento fica registrado, prescricao fica entregue quando houver medicamento, e o historico do paciente e atualizado.

## 17. Regras de negocio principais

### Login

- Usuario precisa informar e-mail e senha.
- Usuario inativo nao acessa.
- Perfil define as telas liberadas.

### Paciente

- Paciente precisa ter nome, CPF, data de nascimento e telefone.
- Recepcao e Admin cadastram pacientes.
- Medico consulta pacientes.
- Apenas Admin remove pacientes.

### Consulta

- Consulta precisa ter paciente, medico e data/hora.
- Consulta nova inicia como Agendada.
- Consulta pode ficar Agendada, Realizada ou Cancelada.

### Prontuario

- Apenas Medico cria prontuario.
- Prontuario precisa estar ligado a um paciente.
- Prontuario deve registrar medico responsavel.

### Prescricao

- Apenas Medico cria prescricao.
- Prescricao precisa estar ligada a um prontuario.
- Prescricao nova inicia como Pendente.
- Prescricao pode ficar Pendente, Entregue ou Cancelada.

### Farmacia

- Apenas Farmacia dispensa medicamento.
- Dispensacao so ocorre para prescricao Pendente.
- Dispensacao baixa estoque.
- Estoque nao pode ficar negativo.

### Estoque

- Farmacia e Admin gerenciam medicamentos.
- Medicamento inativo nao deve entrar em nova prescricao.
- Medicamento com saldo baixo deve gerar alerta.

### Auditoria

- Sistema registra acoes importantes.
- Admin pode consultar auditoria.
- Auditoria mostra usuario, acao, recurso e data/hora.

## 18. O que desenhar primeiro

Para o trabalho, recomendo desenhar nesta ordem:

1. P11 - Fluxo completo de atendimento.
2. P05 - Atendimento medico e prontuario.
3. P06 - Prescricao medica.
4. P07 - Dispensacao de medicamento.
5. P03 e P04 juntos - Cadastro de paciente e agendamento.
6. P10 - Relatorios e auditoria, se precisar mostrar gestao.

Se precisar de poucos diagramas, desenhe apenas:

- Atendimento completo.
- Prescricao e dispensacao.
- Cadastro/agendamento.
- Administracao e auditoria.
