# Bot FURIA

Este é um bot para Telegram que interage com os usuários fornecendo informações sobre a FURIA, como próximos jogos, jogadores, história e formas de contato. Ele também permite que os usuários participem de quizzes rápidos sobre esportes e games, com um sistema de sorteio integrado. O bot também usa o ChatGPT para responder perguntas livres dos usuários.

## Funcionalidades

- **Menu interativo**:
  - Exibe os **próximos jogos** da FURIA.
  - Lista os **jogadores da FURIA** em diferentes modalidades (CS, LoL, Valorant).
  - Apresenta a **história** da FURIA.
  - Fornece os **contatos** da organização.

- **Quiz interativo**:
  - Os usuários podem responder a perguntas rápidas sobre futebol ou jogos.
  - Dependendo da resposta, os usuários podem avançar para o próximo passo do processo (envio de CPF para sorteio ou escolha de jogo a ser acompanhado).

- **Cadastro de usuário**:
  - O bot registra o CPF dos usuários para participar de sorteios, validando o formato do CPF.
  - Os usuários podem escolher um **jogo desejado** (LoL, CS ou Valorant) para acompanhar.

- **Respostas livres com ChatGPT**:
  - O bot usa o **ChatGPT** para responder a perguntas livres dos usuários sobre diversos tópicos, como esportes, games, ou curiosidades. (Não está funcionando pois nao foi pago o acesso para API)

## Instalação

### Pré-requisitos

- Python 3.7 ou superior
- Biblioteca `aiogram` para interação com o Telegram
- Banco de dados SQLite
- Chave de API do **OpenAI** (para o uso do ChatGPT)

### Passos para instalar

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/Hitalo27/ChallengerFuria.git
   cd ChallengerFuria/Challenger 1
   python chatbotFuria.py
