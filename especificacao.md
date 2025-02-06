### Fluxo de Conversas do Aplicativo

#### 0 - Cadastro de Contatos
- **Passo 0:** Verifica se o contato está cadastrado.
  - Se não cadastrado, prossegue para o Passo 1.
- **Passo 1:** Cadastra o número de telefone do contato no sistema.
- **Passo 2:** Solicita o nome do contato via mensagem.
- **Passo 3:** Registra o nome do contato no sistema e confirma o cadastro.

#### 1 - Menu Principal
- **Passo 1:** Exibe o menu principal com opções numeradas.
- **Passo 2:** Se o usuário informar "1", direciona para o fluxo de Coletas.
- **Passo 3:** Se o usuário informar "2", direciona para o fluxo de Cotação.
- **Passo 4:** Se o usuário informar "3", retorna ao cadastro de contatos para edição.
- **Passo 5:** Se o usuário informar "4", exibe opções de suporte.
- **Passo 6:** Se o usuário informar uma opção inválida, exibe mensagem de erro e solicita nova entrada.

#### 2 - Coletas
- **Passo 1:** Solicita o endereço de coleta ao usuário.
- **Passo 2:** Solicita o horário desejado para a coleta.
- **Passo 3:** Confirma os dados da coleta com o usuário.
- **Passo 4:** Registra a solicitação de coleta no sistema e informa o status ao usuário.

#### 3 - Cotação
- **Passo 1:** Solicita informações sobre o volume da carga (peso, dimensões, tipo de mercadoria).
- **Passo 2:** Solicita o endereço de destino para a cotação.
- **Passo 3:** Calcula e exibe o valor estimado da cotação ao usuário.
- **Passo 4:** Pergunta se o usuário deseja confirmar o serviço.
- **Passo 5:** Se confirmado, direciona para o agendamento do serviço.
- **Passo 6:** Se não confirmado, retorna ao menu principal.

#### 4 - Suporte
- **Passo 1:** Exibe as opções de suporte:
  - "1" para Dúvidas Frequentes.
  - "2" para Atendimento Humano.
- **Passo 2:** Direciona o usuário para a opção escolhida.
- **Passo 3:** Se necessário, encaminha o usuário para um atendente humano.

#### 5 - Finalização
- **Passo 1:** Exibe mensagem de agradecimento pelo contato.
- **Passo 2:** Pergunta se o usuário deseja retornar ao menu principal ou encerrar a conversa.
- **Passo 3:** Se o usuário optar por encerrar, finaliza a interação com uma mensagem de despedida.

