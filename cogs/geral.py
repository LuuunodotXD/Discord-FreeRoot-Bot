import discord
from discord import app_commands
from discord.ext import commands
import datetime
from typing import Optional


COMANDOS = {
    "🛡️ Moderação": [
        ("`/ban`", "Bane um usuário"),
        ("`/unban`", "Desbane por ID"),
        ("`/kick`", "Expulsa um usuário"),
        ("`/timeout`", "Silencia temporariamente"),
        ("`/untimeout`", "Remove o timeout"),
        ("`/warn`", "Aplica um aviso"),
        ("`/warnings`", "Ver avisos de um usuário"),
        ("`/clearwarns`", "Limpa avisos (admin)"),
        ("`/clear`", "Apaga mensagens (máx 100)"),
        ("`/slowmode`", "Define o slowmode"),
        ("`/lock` / `/unlock`", "Trava/destrava o canal"),
        ("`/nick`", "Altera o apelido"),
        ("`/banlist`", "Lista os banidos"),
    ],
    "🔧 Utilidade": [
        ("`/ping`", "Latência do bot"),
        ("`/uptime`", "Tempo online"),
        ("`/avatar`", "Avatar de um usuário"),
        ("`/userinfo`", "Informações do usuário"),
        ("`/serverinfo`", "Informações do servidor"),
        ("`/roleinfo`", "Informações de um cargo"),
        ("`/membros`", "Contagem de membros"),
        ("`/cargos`", "Lista os cargos"),
        ("`/enquete`", "Cria uma enquete"),
        ("`/anuncio`", "Faz um anúncio"),
        ("`/embed`", "Cria um embed personalizado"),
        ("`/sugestao`", "Envia uma sugestão"),
    ],
    "🎉 Diversão": [
        ("`/8ball`", "Bola mágica 8"),
        ("`/dado`", "Rola um dado"),
        ("`/coinflip`", "Cara ou coroa"),
        ("`/piada`", "Conta uma piada"),
        ("`/ship`", "Compatibilidade entre dois usuários"),
        ("`/escolher`", "Escolhe uma opção aleatória"),
        ("`/sorteio`", "Realiza um sorteio"),
        ("`/maisantigos`", "Membros mais antigos"),
    ],
}


class Geral(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── PING ──────────────────────────────────────────────────────────────────
    @app_commands.command(name="ping", description="Mostra a latência do bot")
    async def ping(self, interaction: discord.Interaction):
        ms = round(self.bot.latency * 1000)
        cor = (discord.Color.green() if ms < 100
               else discord.Color.orange() if ms < 200
               else discord.Color.red())
        embed = discord.Embed(title="🏓 Pong!", color=cor)
        embed.add_field(name="Latência da API", value=f"`{ms}ms`")
        await interaction.response.send_message(embed=embed)

    # ── UPTIME ────────────────────────────────────────────────────────────────
    @app_commands.command(name="uptime", description="Mostra há quanto tempo o bot está online")
    async def uptime(self, interaction: discord.Interaction):
        delta = datetime.datetime.utcnow() - self.bot.start_time
        total = int(delta.total_seconds())
        dias, resto = divmod(total, 86400)
        horas, resto = divmod(resto, 3600)
        minutos, segundos = divmod(resto, 60)

        partes = []
        if dias:
            partes.append(f"{dias}d")
        if horas:
            partes.append(f"{horas}h")
        if minutos:
            partes.append(f"{minutos}min")
        partes.append(f"{segundos}s")

        embed = discord.Embed(
            title="⏱️ Uptime",
            description=" ".join(partes),
            color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    # ── AVATAR ────────────────────────────────────────────────────────────────
    @app_commands.command(name="avatar", description="Mostra o avatar de um usuário")
    @app_commands.describe(usuario="Usuário (padrão: você mesmo)")
    async def avatar(self, interaction: discord.Interaction,
                     usuario: Optional[discord.Member] = None):
        alvo = usuario or interaction.user
        av = alvo.display_avatar

        embed = discord.Embed(title=f"🖼️ Avatar de {alvo.display_name}", color=discord.Color.blue())
        embed.set_image(url=av.url)
        embed.add_field(
            name="Download",
            value=f"[PNG]({av.with_format('png').url}) • "
                  f"[JPG]({av.with_format('jpg').url}) • "
                  f"[WEBP]({av.with_format('webp').url})")
        await interaction.response.send_message(embed=embed)

    # ── USERINFO ──────────────────────────────────────────────────────────────
    @app_commands.command(name="userinfo", description="Informações detalhadas de um usuário")
    @app_commands.describe(usuario="Usuário (padrão: você mesmo)")
    async def userinfo(self, interaction: discord.Interaction,
                       usuario: Optional[discord.Member] = None):
        m = usuario or interaction.user

        cargos = [r.mention for r in reversed(m.roles) if r.name != "@everyone"]
        cargos_str = " ".join(cargos[:15]) if cargos else "Nenhum"
        if len(cargos) > 15:
            cargos_str += f" … (+{len(cargos) - 15})"

        flags = []
        if m.bot:
            flags.append("🤖 Bot")
        if m.premium_since:
            flags.append(f"💎 Boosting desde {discord.utils.format_dt(m.premium_since, 'D')}")

        embed = discord.Embed(
            title=str(m),
            description=" • ".join(flags) if flags else None,
            color=m.color if m.color.value else discord.Color.blurple())
        embed.set_thumbnail(url=m.display_avatar.url)
        embed.add_field(name="🆔 ID", value=f"`{m.id}`", inline=True)
        embed.add_field(name="🎨 Apelido", value=m.display_name, inline=True)
        embed.add_field(name="📅 Conta criada",
                        value=discord.utils.format_dt(m.created_at, "D"), inline=True)
        embed.add_field(name="📥 Entrou no servidor",
                        value=discord.utils.format_dt(m.joined_at, "D") if m.joined_at else "N/A",
                        inline=True)
        embed.add_field(name="🎨 Cor do cargo",
                        value=str(m.color) if m.color.value else "Padrão", inline=True)
        embed.add_field(name="📌 Cargo mais alto",
                        value=m.top_role.mention, inline=True)
        embed.add_field(name=f"🎭 Cargos ({len(cargos)})",
                        value=cargos_str[:1024], inline=False)
        await interaction.response.send_message(embed=embed)

    # ── SERVERINFO ────────────────────────────────────────────────────────────
    @app_commands.command(name="serverinfo", description="Informações do servidor")
    async def serverinfo(self, interaction: discord.Interaction):
        g = interaction.guild

        verificacao = {
            discord.VerificationLevel.none: "Nenhuma",
            discord.VerificationLevel.low: "Baixa",
            discord.VerificationLevel.medium: "Média",
            discord.VerificationLevel.high: "Alta",
            discord.VerificationLevel.highest: "Máxima",
        }

        embed = discord.Embed(
            title=f"🏠 {g.name}",
            description=g.description or "",
            color=discord.Color.blue())

        if g.icon:
            embed.set_thumbnail(url=g.icon.url)
        if g.banner:
            embed.set_image(url=g.banner.url)

        embed.add_field(name="🆔 ID", value=f"`{g.id}`", inline=True)
        embed.add_field(name="👑 Dono", value=g.owner.mention, inline=True)
        embed.add_field(name="📅 Criado em",
                        value=discord.utils.format_dt(g.created_at, "D"), inline=True)
        embed.add_field(name="👥 Membros",
                        value=f"{g.member_count} total\n"
                              f"{sum(1 for m in g.members if not m.bot)} humanos\n"
                              f"{sum(1 for m in g.members if m.bot)} bots",
                        inline=True)
        embed.add_field(name="💬 Canais",
                        value=f"{len(g.text_channels)} texto\n"
                              f"{len(g.voice_channels)} voz\n"
                              f"{len(g.categories)} categorias",
                        inline=True)
        embed.add_field(name="📊 Outros",
                        value=f"{len(g.roles)} cargos\n"
                              f"{len(g.emojis)} emojis\n"
                              f"{g.premium_subscription_count} boosts (Nível {g.premium_tier})",
                        inline=True)
        embed.add_field(name="🔒 Verificação",
                        value=verificacao.get(g.verification_level, "Desconhecida"), inline=True)
        await interaction.response.send_message(embed=embed)

    # ── ROLEINFO ──────────────────────────────────────────────────────────────
    @app_commands.command(name="roleinfo", description="Informações de um cargo")
    @app_commands.describe(cargo="Cargo")
    async def roleinfo(self, interaction: discord.Interaction, cargo: discord.Role):
        embed = discord.Embed(title=f"🎭 {cargo.name}", color=cargo.color)
        embed.add_field(name="🆔 ID", value=f"`{cargo.id}`", inline=True)
        embed.add_field(name="🎨 Cor", value=str(cargo.color), inline=True)
        embed.add_field(name="👥 Membros", value=len(cargo.members), inline=True)
        embed.add_field(name="📌 Posição", value=cargo.position, inline=True)
        embed.add_field(name="🤖 Gerenciado?", value="Sim" if cargo.managed else "Não", inline=True)
        embed.add_field(name="📣 Mencionável?", value="Sim" if cargo.mentionable else "Não", inline=True)
        embed.add_field(name="📅 Criado em",
                        value=discord.utils.format_dt(cargo.created_at, "D"), inline=True)
        await interaction.response.send_message(embed=embed)

    # ── MEMBROS ───────────────────────────────────────────────────────────────
    @app_commands.command(name="membros", description="Exibe a contagem de membros do servidor")
    async def membros(self, interaction: discord.Interaction):
        g = interaction.guild
        humanos = sum(1 for m in g.members if not m.bot)
        bots = sum(1 for m in g.members if m.bot)
        embed = discord.Embed(title="👥 Membros", color=discord.Color.blue())
        embed.add_field(name="Total", value=g.member_count, inline=True)
        embed.add_field(name="Humanos", value=humanos, inline=True)
        embed.add_field(name="Bots", value=bots, inline=True)
        await interaction.response.send_message(embed=embed)

    # ── CARGOS ────────────────────────────────────────────────────────────────
    @app_commands.command(name="cargos", description="Lista todos os cargos do servidor")
    async def cargos(self, interaction: discord.Interaction):
        cargos = sorted(interaction.guild.roles, key=lambda r: r.position, reverse=True)
        linhas = [
            f"{r.mention} — **{len(r.members)}** membro(s)"
            for r in cargos if r.name != "@everyone"
        ]
        descricao = "\n".join(linhas)[:4000]
        embed = discord.Embed(
            title=f"🎭 Cargos de {interaction.guild.name} ({len(cargos) - 1})",
            description=descricao,
            color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    # ── ENQUETE ───────────────────────────────────────────────────────────────
    @app_commands.command(name="enquete", description="Cria uma enquete com reações")
    @app_commands.describe(
        pergunta="Pergunta da enquete",
        opcoes="Opções separadas por vírgula (ex: Sim,Não,Talvez). Padrão: Sim/Não")
    async def enquete(self, interaction: discord.Interaction,
                      pergunta: str, opcoes: str = "Sim,Não"):
        lista = [o.strip() for o in opcoes.split(",") if o.strip()][:10]
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

        descricao = "\n".join([f"{emojis[i]} {op}" for i, op in enumerate(lista)])
        embed = discord.Embed(
            title=f"📊 {pergunta}",
            description=descricao,
            color=discord.Color.blue())
        embed.set_footer(
            text=f"Enquete de {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)
        msg = await interaction.original_response()

        for i in range(len(lista)):
            await msg.add_reaction(emojis[i])

    # ── ANUNCIO ───────────────────────────────────────────────────────────────
    @app_commands.command(name="anuncio", description="Envia um anúncio formatado em um canal")
    @app_commands.describe(
        canal="Canal de destino",
        titulo="Título do anúncio",
        mensagem="Corpo do anúncio",
        mencionar_todos="Mencionar @everyone?")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def anuncio(self, interaction: discord.Interaction,
                      canal: discord.TextChannel, titulo: str,
                      mensagem: str, mencionar_todos: bool = False):

        embed = discord.Embed(
            title=f"📢 {titulo}",
            description=mensagem,
            color=discord.Color.gold())
        embed.set_footer(
            text=f"Anúncio por {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url)
        embed.timestamp = datetime.datetime.utcnow()

        content = "@everyone" if mencionar_todos else None
        await canal.send(content=content, embed=embed)
        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"✅ Anúncio enviado em {canal.mention}!",
                color=discord.Color.green()),
            ephemeral=True)

    # ── EMBED ─────────────────────────────────────────────────────────────────
    @app_commands.command(name="embed", description="Cria um embed personalizado")
    @app_commands.describe(
        titulo="Título",
        descricao="Descrição",
        cor="Cor em hex (ex: ff6b35). Padrão: azul do Discord",
        canal="Canal de envio (padrão: canal atual)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def embed_cmd(self, interaction: discord.Interaction,
                        titulo: str, descricao: str,
                        cor: str = "5865f2",
                        canal: Optional[discord.TextChannel] = None):
        try:
            cor_int = int(cor.replace("#", ""), 16)
        except ValueError:
            cor_int = 0x5865F2

        embed = discord.Embed(title=titulo, description=descricao, color=cor_int)
        destino = canal or interaction.channel
        await destino.send(embed=embed)
        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"✅ Embed enviado em {destino.mention}!",
                color=discord.Color.green()),
            ephemeral=True)

    # ── SUGESTÃO ──────────────────────────────────────────────────────────────
    @app_commands.command(name="sugestao", description="Envia uma sugestão para o servidor")
    @app_commands.describe(
        sugestao="Sua sugestão",
        canal="Canal de sugestões (padrão: canal atual)")
    async def sugestao(self, interaction: discord.Interaction,
                       sugestao: str,
                       canal: Optional[discord.TextChannel] = None):
        destino = canal or interaction.channel
        embed = discord.Embed(
            title="💡 Nova Sugestão",
            description=sugestao,
            color=discord.Color.yellow())
        embed.set_footer(
            text=f"Sugerido por {interaction.user}",
            icon_url=interaction.user.display_avatar.url)
        embed.timestamp = datetime.datetime.utcnow()

        msg = await destino.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"✅ Sugestão enviada em {destino.mention}!",
                color=discord.Color.green()),
            ephemeral=True)

    # ── AJUDA ─────────────────────────────────────────────────────────────────
    @app_commands.command(name="ajuda", description="Lista todos os comandos disponíveis")
    async def ajuda(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📖 Comandos Disponíveis",
            description="Todos os comandos usam `/`. Clique para ver detalhes no Discord.",
            color=discord.Color.blurple())
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        for categoria, cmds in COMANDOS.items():
            valor = "\n".join([f"{cmd} — {desc}" for cmd, desc in cmds])
            embed.add_field(name=categoria, value=valor, inline=False)

        embed.set_footer(text=f"Total: {sum(len(v) for v in COMANDOS.values())} comandos")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Geral(bot))
