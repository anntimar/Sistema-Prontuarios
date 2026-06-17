# Modelagem BPMN - Regras de negocio e processos

Este documento descreve as regras de negocio, atores, processos e pontos de
decisao do Sistema de Prontuarios. Ele serve como base para criar os diagramas
BPMN do projeto.

O foco aqui e o funcionamento de negocio do sistema, nao detalhes de codigo.
O modo GitHub Pages/localStorage deve ser tratado apenas como ambiente de
demonstracao. Na modelagem BPMN, considere o "Sistema de Prontuarios" como o
sistema que registra, valida e consulta as informacoes.

## 1. Escopo do sistema

O sistema apoia a rotina de uma clinica ou unidade de atendimento, cobrindo:

- Login e controle de acesso por perfil.
- Cadastro e manutencao de pacientes.
- Agendamento e acompanhamento de consultas.
- Registro de prontuarios clinicos.
- Registro e controle de prescricoes.
- Dispensacao de medicamentos pela farmacia.
- Controle basico de estoque de medicamentos.
- Upload ou registro de anexos clinicos.
- Gestao de usuarios.
- Relatorios gerenciais.
- Auditoria operacional.

Fora do escopo atual:

- Integracao com prontuario nacional, SUS ou operadoras.
- Assinatura digital medica.
- Prescricao eletronica oficial.
- Controle financeiro.
- Faturamento hospitalar.
- Internacao, leitos e triagem de emergencia.
- Multiunidade com filiais.

## 2. Atores e responsabilidades

| Ator | Papel no negocio | Responsabilidades principais |
| --- | --- | --- |
| Administrador | Gerencia o sistema | Cadastrar usuarios, revisar relatorios, consultar auditoria, resetar demonstracao quando aplicavel |
| Recepcao | Opera o atendimento inicial | Cadastrar pacientes, atualizar dados cadastrais, agendar consultas, anexar documentos administrativos ou clinicos |
| Medico | Realiza atendimento clinico | Consultar paciente, registrar prontuario, gerar prescricao, marcar consulta como realizada, anexar documentos clinicos |
| Farmacia | Controla medicamentos | Cadastrar medicamentos, controlar estoque, registrar movimentacoes, dispensar prescricoes pendentes |
| Sistema de Prontuarios | Automatiza validacoes e registros | Validar permissoes, salvar dados, atualizar status, gerar historico, registrar auditoria e relatorios |

## 3. Perfis de acesso

| Modulo | Admin | Recepcao | Medico | Farmacia |
| --- | --- | --- | --- | --- |
| Painel | Sim | Sim | Sim | Sim |
| Pacientes | Sim | Sim | Sim, consulta | Nao |
| Prontuarios | Sim, consulta | Sim, consulta | Sim, cria e consulta | Nao |
| Prescricoes | Sim, consulta | Nao | Sim, cria/edita/cancela pendentes | Sim, consulta e dispensa |
| Agenda | Sim | Sim | Sim | Nao |
| Medicamentos/estoque | Sim | Nao | Sim, consulta | Sim, gerencia |
| Usuarios | Sim | Nao | Nao | Nao |
| Relatorios | Sim | Nao | Nao | Nao |
| Auditoria | Sim | Nao | Nao | Nao |

Regras gerais de acesso:

- RN-GER-01: Todo usuario deve estar autenticado para acessar o sistema.
- RN-GER-02: O usuario so pode acessar funcionalidades permitidas ao seu perfil.
- RN-GER-03: Um usuario inativo nao deve conseguir realizar login.
- RN-GER-04: Acoes relevantes devem ser registradas em auditoria.
- RN-GER-05: Dados clinicos devem ser tratados como informacao sensivel.
- RN-GER-06: O sistema deve impedir operacoes com dados obrigatorios ausentes.
- RN-GER-07: Registros nao devem ser alterados por perfis sem permissao.

## 4. Entidades de negocio

| Entidade | Descricao | Principais dados |
| --- | --- | --- |
| Usuario | Pessoa autorizada a acessar o sistema | Nome, e-mail, senha, perfil, status ativo/inativo |
| Paciente | Pessoa atendida pela clinica | Nome, CPF, data de nascimento, telefone |
| Consulta | Agendamento entre paciente e medico | Paciente, medico, data/hora, status, observacoes |
| Prontuario | Registro clinico do atendimento | Paciente, medico, consulta opcional, anamnese, diagnostico, observacoes |
| Prescricao | Orientacao medicamentosa criada pelo medico | Prontuario, medicamentos, quantidades, posologia, status |
| Medicamento | Item controlado pela farmacia | Nome, apresentacao, quantidade, estoque minimo, status ativo |
| Movimentacao de estoque | Entrada ou saida de medicamento | Medicamento, tipo, quantidade, saldo anterior, saldo atual, usuario |
| Anexo clinico | Documento vinculado ao paciente/prontuario | Tipo, titulo, arquivo/link, observacoes, responsavel |
| Auditoria | Registro de acao realizada no sistema | Usuario, acao, recurso, data/hora, metadados |
| Relatorio | Visao gerencial consolidada | Periodo, totais, agrupamentos por status/data |

## 5. Processos para BPMN

Sugestao de diagramas:

1. Processo de autenticacao e controle de acesso.
2. Processo de cadastro e manutencao de paciente.
3. Processo de agendamento de consulta.
4. Processo de atendimento clinico e prontuario.
5. Processo de prescricao e dispensacao de medicamento.
6. Processo de controle de estoque.
7. Processo administrativo: usuarios, relatorios e auditoria.

Tambem e possivel criar um macroprocesso unico chamado "Atendimento clinico",
ligando cadastro, agenda, consulta, prontuario, prescricao e farmacia.

## 6. P01 - Autenticacao e acesso ao sistema

### Objetivo

Permitir que usuarios autorizados acessem o sistema conforme seu perfil.

### Raias BPMN sugeridas

- Usuario
- Sistema de Prontuarios

### Evento inicial

Usuario deseja acessar o sistema.

### Fluxo principal

1. Usuario informa e-mail e senha.
2. Sistema valida se o e-mail existe.
3. Sistema valida se o usuario esta ativo.
4. Sistema valida se a senha esta correta.
5. Sistema inicia a sessao do usuario.
6. Sistema identifica o perfil do usuario.
7. Sistema apresenta o painel e menus permitidos ao perfil.

### Gateways de decisao

- E-mail existe?
- Usuario esta ativo?
- Senha confere?
- Perfil possui permissao para a funcionalidade solicitada?

### Fluxos alternativos e excecoes

- Se e-mail ou senha estiverem incorretos, o sistema informa falha de login.
- Se usuario estiver inativo, o sistema bloqueia acesso.
- Se usuario tentar acessar modulo nao permitido, o sistema nega acesso e mantem o usuario em area permitida.

### Dados usados

- Usuario
- Perfil de acesso
- Sessao/autenticacao
- Registro de auditoria

### Regras de negocio

- RN-AUT-01: Login exige e-mail e senha.
- RN-AUT-02: Usuario inativo nao pode autenticar.
- RN-AUT-03: Cada perfil visualiza apenas os modulos autorizados.
- RN-AUT-04: Tentativas de acoes relevantes podem gerar registro de auditoria.

### Evento final

Usuario autenticado e direcionado para o painel, ou acesso negado.

## 7. P02 - Gestao de usuarios

### Objetivo

Permitir que o administrador crie, edite, ative ou desative usuarios do sistema.

### Raias BPMN sugeridas

- Administrador
- Sistema de Prontuarios

### Evento inicial

Administrador precisa cadastrar ou alterar acesso de um usuario.

### Pre-condicoes

- Administrador esta autenticado.
- Administrador possui permissao para gestao de usuarios.

### Fluxo principal

1. Administrador acessa o modulo Usuarios.
2. Sistema lista usuarios cadastrados.
3. Administrador escolhe criar novo usuario ou editar usuario existente.
4. Administrador informa nome, e-mail, perfil, senha e status.
5. Sistema valida campos obrigatorios.
6. Sistema valida se o e-mail ja esta em uso.
7. Sistema salva o usuario.
8. Sistema registra auditoria da acao.
9. Sistema atualiza a lista de usuarios.

### Gateways de decisao

- Acao e cadastro ou edicao?
- E-mail ja existe?
- Perfil selecionado e valido?
- Usuario deve ficar ativo ou inativo?

### Fluxos alternativos e excecoes

- Se e-mail ja existir, o sistema bloqueia o cadastro.
- Se perfil for invalido, o sistema rejeita a operacao.
- Se senha nao for informada em novo cadastro, o sistema deve impedir a criacao.
- Em edicao, senha vazia mantem a senha anterior.

### Dados usados

- Usuario
- Perfil
- Auditoria

### Regras de negocio

- RN-USU-01: Apenas administrador gerencia usuarios.
- RN-USU-02: E-mail de usuario deve ser unico.
- RN-USU-03: Usuario deve possuir um dos perfis permitidos: admin, medico, farmaceutico ou recepcao.
- RN-USU-04: Usuario inativo nao pode realizar login.
- RN-USU-05: Toda criacao ou alteracao de usuario deve ser auditada.

### Evento final

Usuario cadastrado/atualizado, ou operacao rejeitada por regra de negocio.

## 8. P03 - Cadastro e manutencao de pacientes

### Objetivo

Registrar e manter os dados cadastrais de pacientes atendidos pela clinica.

### Raias BPMN sugeridas

- Recepcao
- Administrador
- Sistema de Prontuarios

### Evento inicial

Paciente procura atendimento ou precisa atualizar seus dados.

### Pre-condicoes

- Usuario autenticado como recepcao ou administrador.

### Fluxo principal

1. Recepcao acessa o modulo Pacientes.
2. Recepcao pesquisa o paciente por nome ou CPF.
3. Sistema exibe pacientes encontrados.
4. Se paciente nao existir, recepcao inicia novo cadastro.
5. Recepcao informa nome, CPF, data de nascimento e telefone.
6. Sistema valida campos obrigatorios.
7. Sistema salva o cadastro do paciente.
8. Sistema registra auditoria.
9. Sistema disponibiliza paciente para agenda, prontuario, anexos e prescricoes.

### Gateways de decisao

- Paciente ja existe?
- Dados obrigatorios estao completos?
- Usuario pode cadastrar/editar pacientes?
- Administrador deseja remover paciente?

### Fluxos alternativos e excecoes

- Se paciente ja existir, recepcao atualiza dados quando necessario.
- Se usuario for medico, pode consultar paciente, mas nao deve alterar cadastro.
- Se administrador remover paciente, o sistema deve considerar impactos em historico clinico.
- Se dados obrigatorios faltarem, o sistema bloqueia o salvamento.

### Dados usados

- Paciente
- Auditoria

### Regras de negocio

- RN-PAC-01: Paciente deve possuir nome, CPF, data de nascimento e telefone.
- RN-PAC-02: Recepcao e admin podem cadastrar e editar pacientes.
- RN-PAC-03: Medico pode consultar pacientes para atendimento.
- RN-PAC-04: Apenas admin pode remover paciente.
- RN-PAC-05: Alteracoes de pacientes devem ser auditadas.

### Evento final

Paciente cadastrado, atualizado, localizado ou remocao concluida conforme permissao.

## 9. P04 - Agendamento e acompanhamento de consultas

### Objetivo

Organizar as consultas entre pacientes e medicos, acompanhando o status do atendimento.

### Raias BPMN sugeridas

- Recepcao
- Medico
- Sistema de Prontuarios

### Evento inicial

Paciente solicita consulta ou clinica precisa agendar atendimento.

### Pre-condicoes

- Paciente cadastrado.
- Medico cadastrado e ativo.
- Usuario autenticado com permissao de agenda.

### Fluxo principal

1. Recepcao acessa Agenda.
2. Sistema lista consultas existentes.
3. Recepcao seleciona paciente e medico.
4. Recepcao informa data/hora e observacoes.
5. Sistema valida dados obrigatorios.
6. Sistema cria consulta com status Agendada.
7. Sistema registra auditoria.
8. Medico acessa sua agenda.
9. Medico atende paciente.
10. Medico atualiza status da consulta para Realizada.
11. Sistema permite gerar prontuario a partir da consulta realizada.

### Gateways de decisao

- Paciente esta cadastrado?
- Medico esta cadastrado e ativo?
- Consulta sera realizada ou cancelada?
- Consulta realizada precisa gerar prontuario?

### Fluxos alternativos e excecoes

- Se paciente nao estiver cadastrado, processo deve retornar ao cadastro de paciente.
- Se consulta for cancelada, status muda para Cancelada e nao deve gerar prontuario como atendimento realizado.
- Se medico ainda nao realizou atendimento, prontuario vinculado a consulta nao deve ser criado pelo fluxo de consulta realizada.
- Se dados de agendamento estiverem incompletos, sistema bloqueia o registro.

### Dados usados

- Paciente
- Usuario medico
- Consulta
- Prontuario
- Auditoria

### Regras de negocio

- RN-CON-01: Consulta deve possuir paciente, medico, data/hora e status.
- RN-CON-02: Consulta nova inicia como Agendada.
- RN-CON-03: Status permitidos: Agendada, Realizada e Cancelada.
- RN-CON-04: Recepcao e admin podem criar/editar consultas.
- RN-CON-05: Medico pode consultar agenda e atualizar status do atendimento.
- RN-CON-06: Prontuario gerado pela agenda deve estar vinculado a uma consulta realizada.

### Evento final

Consulta agendada, realizada, cancelada ou convertida em prontuario.

## 10. P05 - Atendimento clinico e registro de prontuario

### Objetivo

Registrar as informacoes clinicas do atendimento medico.

### Raias BPMN sugeridas

- Medico
- Sistema de Prontuarios

### Evento inicial

Medico inicia atendimento de um paciente.

### Pre-condicoes

- Medico autenticado.
- Paciente cadastrado.
- Consulta pode existir, mas nao e obrigatoria para todo prontuario.

### Fluxo principal

1. Medico acessa lista de pacientes, agenda ou prontuarios.
2. Medico seleciona paciente.
3. Sistema exibe dados do paciente e historico clinico.
4. Medico registra anamnese.
5. Medico registra diagnostico.
6. Medico registra observacoes clinicas.
7. Se atendimento veio da agenda, sistema vincula o prontuario a consulta.
8. Sistema valida campos obrigatorios.
9. Sistema salva prontuario.
10. Sistema registra auditoria.
11. Sistema disponibiliza prontuario para anexos e prescricoes.

### Gateways de decisao

- Paciente selecionado existe?
- Atendimento esta vinculado a consulta?
- Dados clinicos obrigatorios foram preenchidos?
- Sera criada prescricao apos o prontuario?

### Fluxos alternativos e excecoes

- Se paciente nao existir, medico deve solicitar cadastro pela recepcao.
- Se campos obrigatorios estiverem vazios, sistema nao salva prontuario.
- Se medico cancelar o preenchimento, nenhum prontuario e criado.
- Se usuario nao for medico, nao pode criar prontuario.

### Dados usados

- Paciente
- Consulta
- Prontuario
- Auditoria

### Regras de negocio

- RN-PRT-01: Apenas medico cria prontuario.
- RN-PRT-02: Prontuario deve estar associado a um paciente.
- RN-PRT-03: Prontuario deve registrar medico responsavel.
- RN-PRT-04: Anamnese, diagnostico e observacoes compoem o registro clinico.
- RN-PRT-05: Prontuario pode ser vinculado a consulta realizada.
- RN-PRT-06: Prontuario salvo passa a fazer parte do historico clinico do paciente.

### Evento final

Prontuario registrado no historico clinico do paciente.

## 11. P06 - Registro de anexos clinicos

### Objetivo

Associar documentos clinicos ou administrativos ao paciente e, opcionalmente, a um prontuario.

### Raias BPMN sugeridas

- Recepcao
- Medico
- Sistema de Prontuarios

### Evento inicial

Documento precisa ser anexado ao cadastro ou historico do paciente.

### Pre-condicoes

- Paciente cadastrado.
- Usuario com permissao para anexos.

### Fluxo principal

1. Usuario acessa detalhe do paciente.
2. Usuario escolhe adicionar anexo.
3. Usuario informa tipo do anexo: Exame, Laudo, Imagem ou Outro.
4. Usuario informa titulo e observacoes.
5. Usuario envia arquivo ou informa URL externa.
6. Usuario opcionalmente vincula anexo a um prontuario.
7. Sistema valida dados obrigatorios.
8. Sistema salva anexo.
9. Sistema registra responsavel e data/hora.
10. Sistema registra auditoria.
11. Sistema exibe anexo no historico do paciente.

### Gateways de decisao

- Anexo sera por upload ou URL externa?
- Anexo sera vinculado a prontuario?
- Usuario tem permissao para adicionar anexo?
- Admin solicitou exclusao de anexo?

### Fluxos alternativos e excecoes

- Se arquivo/link nao for informado, sistema bloqueia cadastro.
- Se prontuario selecionado nao pertencer ao paciente, sistema deve rejeitar vinculo.
- Se usuario nao tiver permissao, acao nao deve ser exibida ou deve ser negada.
- Apenas admin remove anexos.

### Dados usados

- Paciente
- Prontuario
- Anexo clinico
- Usuario responsavel
- Auditoria

### Regras de negocio

- RN-ANX-01: Anexo deve estar vinculado a um paciente.
- RN-ANX-02: Anexo pode estar vinculado a um prontuario.
- RN-ANX-03: Tipos permitidos: Exame, Laudo, Imagem e Outro.
- RN-ANX-04: Admin, medico e recepcao podem adicionar anexos.
- RN-ANX-05: Apenas admin pode excluir anexos.
- RN-ANX-06: Todo anexo deve registrar usuario responsavel.

### Evento final

Documento anexado ao historico do paciente.

## 12. P07 - Criacao e manutencao de prescricoes

### Objetivo

Permitir que o medico registre prescricoes vinculadas a um prontuario.

### Raias BPMN sugeridas

- Medico
- Sistema de Prontuarios

### Evento inicial

Medico decide prescrever medicamento apos atendimento.

### Pre-condicoes

- Prontuario existente.
- Medico autenticado.
- Medicamento deve existir no estoque quando a prescricao for estruturada.

### Fluxo principal

1. Medico acessa modulo Prescricoes ou detalhe do paciente.
2. Medico seleciona prontuario.
3. Sistema exibe dados do paciente, diagnostico e medico responsavel.
4. Medico seleciona medicamento ativo do estoque.
5. Medico informa quantidade e posologia.
6. Medico pode adicionar mais itens.
7. Sistema valida se ha pelo menos um medicamento.
8. Sistema valida quantidade informada.
9. Sistema salva prescricao com status Pendente.
10. Sistema registra auditoria.
11. Prescricao fica disponivel para farmacia.

### Gateways de decisao

- Prontuario existe?
- Medicamento esta ativo?
- Quantidade solicitada e valida?
- Prescricao esta pendente?
- Medico deseja editar ou cancelar?

### Fluxos alternativos e excecoes

- Se medicamento nao existir ou estiver inativo, nao deve ser selecionado.
- Se quantidade for invalida, sistema bloqueia cadastro.
- Se prescricao estiver Entregue, medico nao deve editar ou cancelar.
- Se prescricao ainda estiver Pendente, medico pode editar ou cancelar.
- Se o medico usar texto livre de medicamento, isso deve ser tratado como compatibilidade, nao como controle estruturado de estoque.

### Dados usados

- Prontuario
- Paciente
- Medicamento
- Prescricao
- Item de prescricao
- Auditoria

### Regras de negocio

- RN-PRE-01: Apenas medico cria prescricoes.
- RN-PRE-02: Prescricao deve estar vinculada a um prontuario.
- RN-PRE-03: Prescricao nova inicia com status Pendente.
- RN-PRE-04: Status permitidos: Pendente, Entregue e Cancelada.
- RN-PRE-05: Prescricao entregue nao pode ser dispensada novamente.
- RN-PRE-06: Prescricao cancelada nao deve entrar na fila de dispensacao.
- RN-PRE-07: Cada item estruturado deve possuir medicamento, quantidade e posologia.

### Evento final

Prescricao criada, editada, cancelada ou enviada para fila da farmacia.

## 13. P08 - Dispensacao de medicamentos pela farmacia

### Objetivo

Permitir que a farmacia entregue medicamentos prescritos e atualize automaticamente o estoque.

### Raias BPMN sugeridas

- Farmacia
- Sistema de Prontuarios

### Evento inicial

Paciente apresenta prescricao pendente ou farmacia consulta fila de prescricoes.

### Pre-condicoes

- Prescricao com status Pendente.
- Farmaceutico autenticado.
- Medicamentos cadastrados e ativos.

### Fluxo principal

1. Farmacia acessa fila de prescricoes pendentes.
2. Sistema lista prescricoes com paciente, medico, diagnostico e itens.
3. Farmacia seleciona prescricao.
4. Sistema verifica itens e quantidades.
5. Sistema verifica saldo de estoque de cada medicamento.
6. Farmacia confirma dispensacao.
7. Sistema baixa o estoque dos medicamentos.
8. Sistema registra movimentacao do tipo Saida.
9. Sistema altera status da prescricao para Entregue.
10. Sistema registra data/hora de dispensacao.
11. Sistema registra auditoria.

### Gateways de decisao

- Prescricao esta pendente?
- Medicamento esta ativo?
- Ha estoque suficiente?
- Todos os itens podem ser entregues?

### Fluxos alternativos e excecoes

- Se prescricao estiver Entregue, o sistema impede nova dispensacao.
- Se prescricao estiver Cancelada, farmacia nao deve dispensar.
- Se nao houver estoque suficiente, sistema deve bloquear ou sinalizar impossibilidade de entrega completa.
- Se algum medicamento estiver inativo, farmacia deve revisar estoque antes da entrega.

### Dados usados

- Prescricao
- Item de prescricao
- Medicamento
- Movimentacao de estoque
- Auditoria

### Regras de negocio

- RN-DIS-01: Apenas farmacia pode dispensar prescricao.
- RN-DIS-02: Apenas prescricoes Pendentes podem ser dispensadas.
- RN-DIS-03: Dispensacao gera baixa de estoque.
- RN-DIS-04: Cada baixa gera movimentacao de estoque do tipo Saida.
- RN-DIS-05: Prescricao dispensada muda para status Entregue.
- RN-DIS-06: Sistema deve evitar saldo negativo de medicamento.

### Evento final

Medicamentos entregues, estoque atualizado e prescricao marcada como Entregue.

## 14. P09 - Controle de estoque de medicamentos

### Objetivo

Manter o cadastro e o saldo dos medicamentos disponiveis para prescricao e dispensacao.

### Raias BPMN sugeridas

- Farmacia
- Administrador
- Sistema de Prontuarios

### Evento inicial

Farmacia precisa cadastrar medicamento ou movimentar estoque.

### Pre-condicoes

- Usuario autenticado como farmacia ou admin.

### Fluxo principal

1. Farmacia acessa modulo Medicamentos.
2. Sistema lista medicamentos cadastrados e saldos.
3. Farmacia cria ou edita medicamento.
4. Farmacia informa nome, apresentacao, quantidade inicial, estoque minimo e status ativo.
5. Sistema valida dados obrigatorios.
6. Sistema salva medicamento.
7. Quando houver entrada ou saida manual, farmacia registra movimentacao.
8. Sistema calcula saldo anterior e saldo atual.
9. Sistema identifica se medicamento ficou abaixo do estoque minimo.
10. Sistema registra auditoria.

### Gateways de decisao

- Acao e cadastro, edicao ou movimentacao?
- Movimentacao e Entrada ou Saida?
- Saida possui saldo suficiente?
- Saldo atual esta abaixo do minimo?
- Medicamento esta ativo?

### Fluxos alternativos e excecoes

- Se quantidade da saida for maior que saldo, sistema deve bloquear a movimentacao.
- Se medicamento for inativado, nao deve ser usado em novas prescricoes estruturadas.
- Se estoque ficar baixo, sistema sinaliza alerta no painel/modulo.
- Medico pode consultar medicamentos, mas nao gerencia estoque.

### Dados usados

- Medicamento
- Movimentacao de estoque
- Usuario responsavel
- Auditoria

### Regras de negocio

- RN-EST-01: Admin e farmacia podem gerenciar medicamentos.
- RN-EST-02: Medicamento deve possuir nome, apresentacao, quantidade e estoque minimo.
- RN-EST-03: Toda movimentacao altera saldo do medicamento.
- RN-EST-04: Saida nao pode gerar saldo negativo.
- RN-EST-05: Medicamento com quantidade menor ou igual ao estoque minimo deve ser sinalizado como baixo estoque.
- RN-EST-06: Medicamento inativo nao deve ser selecionado em novas prescricoes.

### Evento final

Medicamento cadastrado/atualizado ou estoque movimentado com saldo recalculado.

## 15. P10 - Relatorios gerenciais e auditoria

### Objetivo

Permitir que o administrador acompanhe indicadores do sistema e rastreie acoes operacionais.

### Raias BPMN sugeridas

- Administrador
- Sistema de Prontuarios

### Evento inicial

Administrador precisa analisar dados da operacao ou auditar uma acao.

### Pre-condicoes

- Administrador autenticado.
- Dados operacionais registrados.

### Fluxo principal - relatorios

1. Administrador acessa modulo Relatorios.
2. Administrador informa periodo de analise, quando necessario.
3. Sistema consolida totais do periodo.
4. Sistema agrupa prescricoes por status.
5. Sistema agrupa consultas por status.
6. Sistema agrupa pacientes, prontuarios, consultas e movimentacoes por data.
7. Sistema exibe indicadores.
8. Administrador pode exportar CSV.
9. Administrador pode imprimir relatorio para PDF pelo navegador.

### Fluxo principal - auditoria

1. Administrador acessa modulo Auditoria.
2. Administrador informa filtros: usuario, acao, recurso e periodo.
3. Sistema lista registros de auditoria.
4. Administrador analisa data/hora, usuario, perfil, acao e recurso afetado.
5. Sistema permite rastrear a origem de operacoes relevantes.

### Gateways de decisao

- Administrador deseja relatorio ou auditoria?
- Periodo foi informado?
- Existem dados para os filtros selecionados?
- Administrador deseja exportar/imprimir?

### Fluxos alternativos e excecoes

- Se nao houver dados no periodo, sistema exibe estado vazio.
- Se filtros nao retornarem auditoria, sistema informa ausencia de registros.
- Usuarios nao administradores nao acessam relatorios nem auditoria.

### Dados usados

- Pacientes
- Prontuarios
- Prescricoes
- Consultas
- Medicamentos
- Movimentacoes de estoque
- Usuarios
- Auditoria

### Regras de negocio

- RN-REL-01: Apenas admin acessa relatorios gerenciais.
- RN-REL-02: Relatorios devem respeitar periodo informado.
- RN-REL-03: Indicadores devem ser calculados a partir dos registros operacionais.
- RN-AUD-01: Apenas admin consulta auditoria.
- RN-AUD-02: A auditoria deve conter usuario, perfil, acao, recurso e data/hora.
- RN-AUD-03: Acoes de criacao, edicao, cancelamento, dispensacao e movimentacao devem ser rastreaveis.

### Evento final

Relatorio analisado/exportado ou auditoria consultada.

## 16. P11 - Reset de demonstracao

Este processo existe apenas para ambiente demonstrativo.

### Objetivo

Restaurar a base de demonstracao para dados iniciais.

### Raias BPMN sugeridas

- Administrador
- Sistema de Prontuarios

### Fluxo principal

1. Administrador acessa o painel.
2. Administrador solicita reset da demonstracao.
3. Sistema solicita confirmacao.
4. Administrador confirma.
5. Sistema restaura os dados iniciais.
6. Sistema recarrega os dados da interface.

### Regras de negocio

- RN-DEM-01: Apenas admin pode resetar demonstracao.
- RN-DEM-02: Reset apaga alteracoes feitas durante testes.
- RN-DEM-03: Reset nao deve ser representado como processo clinico real em BPMN final de negocio, salvo se o objetivo for documentar o prototipo.

## 17. Macroprocesso sugerido: Atendimento clinico completo

Este fluxo pode ser usado como diagrama principal.

### Raias sugeridas

- Recepcao
- Medico
- Farmacia
- Sistema de Prontuarios

### Fluxo macro

1. Paciente solicita atendimento.
2. Recepcao pesquisa paciente.
3. Gateway: paciente cadastrado?
4. Se nao, recepcao cadastra paciente.
5. Recepcao agenda consulta.
6. Sistema registra consulta como Agendada.
7. Medico acessa agenda.
8. Medico realiza atendimento.
9. Medico altera consulta para Realizada.
10. Medico registra prontuario.
11. Gateway: atendimento exige prescricao?
12. Se sim, medico registra prescricao.
13. Sistema envia prescricao para fila da farmacia.
14. Farmacia verifica prescricao pendente.
15. Gateway: estoque suficiente?
16. Se sim, farmacia dispensa medicamento.
17. Sistema baixa estoque e marca prescricao como Entregue.
18. Sistema registra auditoria e atualiza relatorios.
19. Processo finaliza com atendimento documentado.

### Excecoes no macroprocesso

- Paciente sem cadastro: retorna para cadastro.
- Consulta cancelada: finaliza sem atendimento clinico.
- Prontuario incompleto: retorna para preenchimento medico.
- Prescricao cancelada: nao segue para dispensacao.
- Estoque insuficiente: farmacia registra impedimento operacional e nao entrega ate regularizar estoque.

## 18. Matriz de rastreabilidade

| Processo | Modulos do sistema | Atores principais | Resultado |
| --- | --- | --- | --- |
| P01 Autenticacao | Login, painel | Todos | Sessao iniciada ou acesso negado |
| P02 Usuarios | Usuarios | Admin | Usuario criado/alterado |
| P03 Pacientes | Pacientes | Recepcao, Admin | Paciente cadastrado/atualizado |
| P04 Agenda | Consultas | Recepcao, Medico | Consulta agendada/realizada/cancelada |
| P05 Prontuario | Prontuarios, Paciente detalhe | Medico | Atendimento registrado |
| P06 Anexos | Paciente detalhe, Anexos | Recepcao, Medico, Admin | Documento vinculado |
| P07 Prescricao | Prescricoes | Medico | Prescricao pendente/cancelada |
| P08 Dispensacao | Prescricoes, Medicamentos | Farmacia | Medicamento entregue e estoque baixado |
| P09 Estoque | Medicamentos | Farmacia, Admin | Saldo atualizado |
| P10 Relatorios/Auditoria | Relatorios, Auditoria | Admin | Indicadores e rastreabilidade |
| P11 Reset demo | Painel | Admin | Dados de demo restaurados |

## 19. Elementos BPMN recomendados

Use os seguintes elementos na criacao dos diagramas:

### Eventos de inicio

- Usuario deseja acessar sistema.
- Paciente solicita atendimento.
- Administrador precisa gerenciar usuarios.
- Farmacia precisa dispensar prescricao.
- Administrador solicita relatorio/auditoria.

### Eventos de fim

- Acesso concedido.
- Acesso negado.
- Paciente cadastrado.
- Consulta agendada.
- Atendimento registrado.
- Prescricao dispensada.
- Estoque atualizado.
- Relatorio emitido.

### Tarefas de usuario

- Informar e-mail e senha.
- Cadastrar paciente.
- Agendar consulta.
- Registrar prontuario.
- Registrar prescricao.
- Confirmar dispensacao.
- Cadastrar medicamento.
- Consultar auditoria.

### Tarefas de sistema

- Validar credenciais.
- Verificar permissao.
- Salvar registro.
- Atualizar status.
- Calcular saldo de estoque.
- Registrar auditoria.
- Consolidar relatorio.

### Gateways exclusivos

- Credenciais validas?
- Usuario ativo?
- Perfil autorizado?
- Paciente ja cadastrado?
- Consulta realizada?
- Prescricao necessaria?
- Prescricao pendente?
- Estoque suficiente?
- Medicamento ativo?
- Dados obrigatorios preenchidos?

### Objetos de dados

- Cadastro do paciente.
- Agendamento da consulta.
- Prontuario clinico.
- Prescricao.
- Medicamento.
- Movimentacao de estoque.
- Anexo clinico.
- Registro de auditoria.
- Relatorio gerencial.

## 20. Checklist para desenhar o BPMN

Antes de finalizar cada diagrama, confira:

- O processo possui evento inicial e evento final claros.
- Cada raia representa um ator real ou o sistema.
- As tarefas humanas estao na raia do ator correto.
- As validacoes automatizadas estao na raia do sistema.
- Gateways possuem perguntas objetivas.
- Todo gateway possui ao menos duas saidas nomeadas.
- Fluxos de excecao estao representados.
- Dados importantes aparecem como objetos de dados ou anotacoes.
- O processo nao mistura detalhe tecnico de tela/API com regra de negocio.
- O final do processo deixa claro o resultado gerado.

## 21. Priorizacao para entrega academica

Se o trabalho exigir poucos diagramas, priorize:

1. Atendimento clinico completo.
2. Prescricao e dispensacao de medicamentos.
3. Gestao de pacientes e agenda.
4. Gestao administrativa, relatorios e auditoria.

Se o trabalho exigir detalhamento maior, use cada processo P01 a P11 como um
diagrama separado.
