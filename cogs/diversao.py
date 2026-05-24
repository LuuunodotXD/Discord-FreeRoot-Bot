import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
import datetime


RESPOSTAS_8BALL = [
    ("✅ Com certeza!", True),
    ("✅ Definitivamente sim!", True),
    ("✅ Sem dúvida!", True),
    ("✅ Sim, pode apostar!", True),
    ("✅ Claro!", True),
    ("🤔 Não sei dizer agora...", False),
    ("🤔 Tente novamente mais tarde.", False),
    ("🤔 Não consigo prever agora.", False),
    ("🤔 Eu acho que não.", False),
    ("❌ Não conte com isso.", False),
    ("❌ Minha resposta é não.", False),
    ("❌ Definitivamente não.", False),
    ("❌ Nem fudendo!", False),
]

PIADAS = [
    ("Por que o livro de matemática foi ao psicólogo?",
     "Porque tinha muitos problemas."),
    ("O que o zero disse pro oito?",
     "Que cinto bonito!"),
    ("Por que o espantalho ganhou um prêmio?",
     "Porque era destacado no seu campo."),
    ("Como se chama um peixe sem olho?",
     "Px."),
    ("O que o oceano disse para a praia?",
     "Nada, só deu uma onda."),
    ("Por que o computador foi ao médico?",
     "Porque estava com vírus."),
    ("O que o DJ disse antes de sair?",
     "Vou dar um drop."),
    ("Por que o elefante não usa computador?",
     "Porque tem medo do mouse."),
    ("O que é um peixe elétrico?",
     "Um plugueixe."),
    ("Por que o astronauta não conseguiu namorar?",
     "Porque precisava de espaço."),
    ("O que o documentário disse para o filme de ação?",
     "Você não tem fundo."),
    ("Por que a vassoura foi promovida?",
     "Porque varreu a concorrência."),
]


class Diversao(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── 8BALL ─────────────────────────────────────────────────────────────────
    @app_commands.command(name="8ball", description="Faça uma pergunta à bola mágica")
    @app_commands.describe(pergunta="Sua pergunta de sim ou não")
    async def bola8(self, interaction: discord.Interaction, pergunta: str):
        resposta, positiva = random.choice(RESPOSTAS_8BALL)
        cor = discord.Color.green() if positiva else discord.Color.red()

        embed = discord.Embed(color=cor)
        embed.add_field(name="❓ Pergunta", value=pergunta, inline=False)
        embed.add_field(name="🎱 Resposta", value=f"**{resposta}**", inline=False)
        await interaction.response.send_message(embed=embed)

    # ── DADO ──────────────────────────────────────────────────────────────────
    @app_commands.command(name="dado", description="Rola um dado")
    @app_commands.describe(lados="Número de lados (padrão: 6)", quantidade="Quantos dados (padrão: 1)")
    async def dado(self, interaction: discord.Interaction,
                   lados: int = 6, quantidade: int = 1):
        if lados < 2:
            return await interaction.response.send_message(
                "O dado precisa ter pelo menos 2 lados!", ephemeral=True)
        if quantidade < 1 or quantidade > 10:
            return await interaction.response.send_message(
                "Role entre 1 e 10 dados por vez.", ephemeral=True)

        resultados = [random.randint(1, lados) for _ in range(quantidade)]
        soma = sum(resultados)

        embed = discord.Embed(title="🎲 Dados Rolados!", color=discord.Color.blue())
        embed.add_field(name="Dados", value=" + ".join([f"`{r}`" for r in resultados]))
        if quantidade > 1:
            embed.add_field(name="Soma", value=f"**{soma}**")
        await interaction.response.send_message(embed=embed)

    # ── COINFLIP ──────────────────────────────────────────────────────────────
    @app_commands.command(name="coinflip", description="Cara ou coroa")
    async def coinflip(self, interaction: discord.Interaction):
        resultado = random.choice([("Cara", "🪙"), ("Coroa", "⚙️")])
        embed = discord.Embed(
            title="🪙 Cara ou Coroa",
            description=f"Resultado: **{resultado[0]}** {resultado[1]}",
            color=discord.Color.gold())
        await interaction.response.send_message(embed=embed)

    # ── PIADA ─────────────────────────────────────────────────────────────────
    @app_commands.command(name="piada", description="Conta uma piada aleatória")
    async def piada(self, interaction: discord.Interaction):
        pergunta, resposta = random.choice(PIADAS)
        embed = discord.Embed(color=discord.Color.yellow())
        embed.add_field(name="😄 Piada", value=pergunta, inline=False)
        embed.add_field(name="💡 Resposta", value=f"||{resposta}||", inline=False)
        embed.set_footer(text="Clique na resposta para revelar!")
        await interaction.response.send_message(embed=embed)

    # ── SHIP ──────────────────────────────────────────────────────────────────
    @app_commands.command(name="ship", description="Calcula a compatibilidade entre dois usuários")
    @app_commands.describe(usuario1="Primeiro usuário", usuario2="Segundo usuário")
    async def ship(self, interaction: discord.Interaction,
                   usuario1: discord.Member, usuario2: discord.Member):

        # Seed determinística para resultado sempre igual para o mesmo par
        seed = (min(usuario1.id, usuario2.id) * 31 + max(usuario1.id, usuario2.id)) % 101
        porcento = seed

        if porcento >= 85:
            emoji, desc, cor = "💞", "Ship perfeito! São feitos um para o outro!", discord.Color.red()
        elif porcento >= 65:
            emoji, desc, cor = "❤️", "Bom ship! Vale tentar!", discord.Color.red()
        elif porcento >= 45:
            emoji, desc, cor = "💛", "Mais ou menos... pode ser!", discord.Color.yellow()
        elif porcento >= 25:
            emoji, desc, cor = "😬", "Meh, complicado... vai precisar se esforçar.", discord.Color.orange()
        else:
            emoji, desc, cor = "💔", "Hmm, não parece muito promissor...", discord.Color.dark_gray()

        cheios = porcento // 10
        barra = "█" * cheios + "░" * (10 - cheios)

        nome_ship = (usuario1.display_name[:len(usuario1.display_name)//2] +
                     usuario2.display_name[len(usuario2.display_name)//2:])

        embed = discord.Embed(
            title=f"💕 {usuario1.display_name} & {usuario2.display_name}",
            description=(f"**Ship name:** {nome_ship}\n\n"
                         f"{emoji} **{porcento}%** — {desc}\n"
                         f"`{barra}`"),
            color=cor)
        embed.set_thumbnail(url=usuario1.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    # ── ESCOLHER ──────────────────────────────────────────────────────────────
    @app_commands.command(name="escolher", description="Escolhe aleatoriamente entre as opções")
    @app_commands.describe(opcoes="Opções separadas por vírgula (ex: Pizza,Hambúrguer,Sushi)")
    async def escolher(self, interaction: discord.Interaction, opcoes: str):
        lista = [o.strip() for o in opcoes.split(",") if o.strip()]
        if len(lista) < 2:
            return await interaction.response.send_message(
                "Insira pelo menos 2 opções separadas por vírgula!", ephemeral=True)

        escolha = random.choice(lista)
        embed = discord.Embed(
            title="🎯 Escolha Aleatória",
            description=(f"De **{len(lista)}** opções, escolhi:\n\n"
                         f"# {escolha}"),
            color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    # ── SORTEIO ───────────────────────────────────────────────────────────────
    @app_commands.command(name="sorteio", description="Inicia um sorteio no canal")
    @app_commands.describe(
        minutos="Duração em minutos",
        premio="Prêmio do sorteio",
        vencedores="Número de vencedores (padrão: 1)")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def sorteio(self, interaction: discord.Interaction,
                      minutos: int, premio: str, vencedores: int = 1):

        if minutos < 1 or minutos > 10080:  # max 7 dias
            return await interaction.response.send_message(
                "A duração deve ser entre 1 e 10080 minutos (7 dias).", ephemeral=True)

        fim = discord.utils.utcnow() + datetime.timedelta(minutes=minutos)
        embed = discord.Embed(
            title="🎉 SORTEIO!",
            description=(f"**Prêmio:** {premio}\n"
                         f"**Vencedores:** {vencedores}\n\n"
                         f"Reaja com 🎉 para participar!\n"
                         f"**Encerra:** {discord.utils.format_dt(fim, 'R')}"),
            color=discord.Color.gold())
        embed.set_footer(
            text=f"Sorteio criado por {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)
        msg = await interaction.original_response()
        await msg.add_reaction("🎉")

        # Finaliza de forma assíncrona sem bloquear
        async def finalizar():
            await asyncio.sleep(minutos * 60)
            try:
                msg_att = await interaction.channel.fetch_message(msg.id)
                reacao = discord.utils.get(msg_att.reactions, emoji="🎉")
                participantes = []
                if reacao:
                    async for user in reacao.users():
                        if not user.bot:
                            participantes.append(user)

                embed_fim = discord.Embed(color=discord.Color.gold())
                embed_fim.set_footer(text=f"Sorteio encerrado • Prêmio: {premio}")

                if len(participantes) >= 1:
                    ganhadores = random.sample(
                        participantes, min(vencedores, len(participantes)))
                    mencoes = " ".join(g.mention for g in ganhadores)
                    embed_fim.title = "🎊 Sorteio Encerrado!"
                    embed_fim.description = (
                        f"**Prêmio:** {premio}\n"
                        f"**{'Vencedor' if len(ganhadores) == 1 else 'Vencedores'}:** "
                        f"{mencoes}\n\nParabéns! 🎉")
                    await interaction.channel.send(
                        content=mencoes,
                        embed=embed_fim)
                else:
                    embed_fim.title = "😢 Sorteio Encerrado"
                    embed_fim.description = "Ninguém participou do sorteio."
                    await interaction.channel.send(embed=embed_fim)
            except Exception as e:
                print(f"Erro ao finalizar sorteio: {e}")

        asyncio.create_task(finalizar())

    # ── MAIS ANTIGOS ──────────────────────────────────────────────────────────
    @app_commands.command(name="maisantigos", description="Mostra os membros mais antigos do servidor")
    async def maisantigos(self, interaction: discord.Interaction):
        membros = [m for m in interaction.guild.members if m.joined_at and not m.bot]
        membros.sort(key=lambda m: m.joined_at)
        top = membros[:15]

        medalhas = {1: "🥇", 2: "🥈", 3: "🥉"}
        linhas = []
        for i, m in enumerate(top, 1):
            icone = medalhas.get(i, f"**{i}.**")
            linhas.append(
                f"{icone} {m.mention} — entrou {discord.utils.format_dt(m.joined_at, 'D')}")

        embed = discord.Embed(
            title=f"🏆 Membros mais antigos de {interaction.guild.name}",
            description="\n".join(linhas),
            color=discord.Color.gold())
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Diversao(bot))
