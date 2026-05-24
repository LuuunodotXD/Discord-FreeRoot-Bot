# 🤖 Bot Discord — Python

Bot completo com slash commands, moderação e diversão.

## 📁 Estrutura

```
discord-bot/
├── main.py              # Arquivo principal
├── requirements.txt     # Dependências
├── .env                 # Token (NÃO commitar!)
├── .env.example         # Modelo do .env
├── dados/
│   └── avisos.json      # Avisos dos usuários (gerado automaticamente)
└── cogs/
    ├── moderacao.py     # Comandos de moderação
    ├── geral.py         # Comandos utilitários
    └── diversao.py      # Comandos de diversão
```

## ⚙️ Instalação

```bash
# 1. Instale as dependências
pip install -r requirements.txt

# 2. Configure o token
cp .env.example .env
# Edite o .env e coloque seu token

# 3. Inicie o bot
python main.py
```

## 🔑 Configuração no Discord Developer Portal

1. Acesse https://discord.com/developers/applications
2. Crie um novo aplicativo → vá em **Bot**
3. Copie o **Token** e cole no `.env`
4. Ative os **Privileged Intents**:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
5. Vá em **OAuth2 → URL Generator**
   - Scopes: `bot` + `applications.commands`
   - Permissões: Administrator (ou selecione manualmente)
   - Acesse o link gerado para adicionar o bot ao servidor

## 📋 Comandos

### 🛡️ Moderação
| Comando | Descrição | Permissão |
|---------|-----------|-----------|
| `/ban` | Bane um usuário | Ban Members |
| `/unban` | Desbane por ID | Ban Members |
| `/kick` | Expulsa um usuário | Kick Members |
| `/timeout` | Silencia temporariamente | Moderate Members |
| `/untimeout` | Remove o timeout | Moderate Members |
| `/warn` | Aplica um aviso | Moderate Members |
| `/warnings` | Ver avisos de um usuário | Moderate Members |
| `/clearwarns` | Limpa todos os avisos | Administrator |
| `/clear` | Apaga mensagens (máx 100) | Manage Messages |
| `/slowmode` | Define o slowmode | Manage Channels |
| `/lock` | Trava o canal | Manage Channels |
| `/unlock` | Destrava o canal | Manage Channels |
| `/nick` | Altera apelido | Manage Nicknames |
| `/banlist` | Lista os banidos | Ban Members |

### 🔧 Utilidade
| Comando | Descrição |
|---------|-----------|
| `/ping` | Latência do bot |
| `/uptime` | Tempo online |
| `/avatar` | Avatar de um usuário |
| `/userinfo` | Informações do usuário |
| `/serverinfo` | Informações do servidor |
| `/roleinfo` | Informações de um cargo |
| `/membros` | Contagem de membros |
| `/cargos` | Lista os cargos |
| `/enquete` | Cria uma enquete com reações |
| `/anuncio` | Faz um anúncio em um canal |
| `/embed` | Cria um embed personalizado |
| `/sugestao` | Envia uma sugestão |
| `/ajuda` | Lista todos os comandos |

### 🎉 Diversão
| Comando | Descrição |
|---------|-----------|
| `/8ball` | Bola mágica 8 |
| `/dado` | Rola dados |
| `/coinflip` | Cara ou coroa |
| `/piada` | Conta uma piada |
| `/ship` | Compatibilidade entre dois usuários |
| `/escolher` | Escolhe uma opção aleatória |
| `/sorteio` | Realiza um sorteio |
| `/maisantigos` | Membros mais antigos |

## 📝 Notas

- Os avisos são salvos em `dados/avisos.json` e persistem entre reinicializações.
- Os slash commands podem demorar até 1 hora para aparecer globalmente.
  Para testes rápidos, use sincronização por guild (veja a documentação do discord.py).
- Nunca compartilhe ou commite seu arquivo `.env`.
