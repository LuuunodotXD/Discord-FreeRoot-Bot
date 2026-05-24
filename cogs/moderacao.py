import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import datetime
from typing import Optional


# ─── Helpers de persistência de avisos ────────────────────────────────────────

def carregar_avisos() -> dict:
    caminho = "dados/avisos.json"
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def salvar_avisos(data: dict):
    os.makedirs("dados", exist_ok=True)
    with open("dados/avisos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ─── Cog ──────────────────────────────────────────────────────────────────────

class Moderacao(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Embeds padrão
    def ok(self, titulo: str, desc: str) -> discord.Embed:
        return discord.Embed(title=titulo, description=desc, color=discord.Color.green())

    def erro(self, desc: str) -> discord.Embed:
        return discord.Embed(title="❌ Erro", description=desc, color=discord.Color.red())

    # ── BAN ───────────────────────────────────────────────────────────────────
    @app_commands.command(name="ban", description="Bane um usuário do servidor")
    @app_commands.describe(usuario="Usuário a banir", motivo="Motivo do ban")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction,
                  usuario: discord.Member, motivo: str = "Não especificado"):

        if usuario.top_role >= interaction.user.top_role:
            return await interaction.response.send_message(
                embed=self.erro("Você não pode banir alguém com cargo igual ou superior ao seu."),
                ephemeral=True)

        try:
            await usuario.send(
                f"🔨 Você foi **banido** de **{interaction.guild.name}**.\n**Motivo:** {motivo}")
        except Exception:
            pass

        await usuario.ban(reason=f"{interaction.user} | {motivo}", delete_message_days=0)
        await interaction.response.send_message(embed=self.ok(
            "🔨 Usuário Banido",
            f"**Usuário:** {usuario.mention}\n**Motivo:** {motivo}\n**Mod:** {interaction.user.mention}"))

    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                embed=self.erro("Você não tem permissão para banir."), ephemeral=True)

    # ── UNBAN ─────────────────────────────────────────────────────────────────
    @app_commands.command(name="unban", description="Desbane um usuário pelo ID")
    @app_commands.describe(user_id="ID do usuário")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        try:
            user = await self.bot.fetch_user(int(user_id))
            await interaction.guild.unban(user)
            await interaction.response.send_message(
                embed=self.ok("✅ Desbanido", f"**{user}** foi desbanido."))
        except discord.NotFound:
            await interaction.response.send_message(
                embed=self.erro("Usuário não encontrado ou não está banido."), ephemeral=True)
        except ValueError:
            await interaction.response.send_message(
                embed=self.erro("ID inválido."), ephemeral=True)

    # ── KICK ──────────────────────────────────────────────────────────────────
    @app_commands.command(name="kick", description="Expulsa um usuário do servidor")
    @app_commands.describe(usuario="Usuário a expulsar", motivo="Motivo")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction,
                   usuario: discord.Member, motivo: str = "Não especificado"):

        if usuario.top_role >= interaction.user.top_role:
            return await interaction.response.send_message(
                embed=self.erro("Você não pode expulsar alguém com cargo igual ou superior ao seu."),
                ephemeral=True)

        try:
            await usuario.send(
                f"👢 Você foi **expulso** de **{interaction.guild.name}**.\n**Motivo:** {motivo}")
        except Exception:
            pass

        await usuario.kick(reason=f"{interaction.user} | {motivo}")
        await interaction.response.send_message(embed=self.ok(
            "👢 Usuário Expulso",
            f"**Usuário:** {usuario.mention}\n**Motivo:** {motivo}\n**Mod:** {interaction.user.mention}"))

    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                embed=self.erro("Você não tem permissão para expulsar."), ephemeral=True)

    # ── TIMEOUT ───────────────────────────────────────────────────────────────
    @app_commands.command(name="timeout", description="Silencia um usuário temporariamente")
    @app_commands.describe(usuario="Usuário", minutos="Duração em minutos", motivo="Motivo")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction,
                      usuario: discord.Member, minutos: int,
                      motivo: str = "Não especificado"):

        if minutos < 1 or minutos > 40320:  # máx 28 dias (limite do Discord)
            return await interaction.response.send_message(
                embed=self.erro("A duração deve ser entre 1 e 40320 minutos (28 dias)."),
                ephemeral=True)

        duracao = datetime.timedelta(minutes=minutos)
        await usuario.timeout(duracao, reason=motivo)

        tempo_str = f"{minutos} minuto(s)"
        if minutos >= 60:
            horas = minutos // 60
            mins = minutos % 60
            tempo_str = f"{horas}h{f' {mins}min' if mins else ''}"

        await interaction.response.send_message(embed=self.ok(
            "⏰ Timeout Aplicado",
            f"**Usuário:** {usuario.mention}\n**Duração:** {tempo_str}\n**Motivo:** {motivo}"))

    # ── UNTIMEOUT ─────────────────────────────────────────────────────────────
    @app_commands.command(name="untimeout", description="Remove o timeout de um usuário")
    @app_commands.describe(usuario="Usuário")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def untimeout(self, interaction: discord.Interaction, usuario: discord.Member):
        await usuario.timeout(None)
        await interaction.response.send_message(embed=self.ok(
            "✅ Timeout Removido",
            f"O timeout de {usuario.mention} foi removido."))

    # ── WARN ──────────────────────────────────────────────────────────────────
    @app_commands.command(name="warn", description="Aplica um aviso a um usuário")
    @app_commands.describe(usuario="Usuário a avisar", motivo="Motivo do aviso")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(self, interaction: discord.Interaction,
                   usuario: discord.Member, motivo: str):

        avisos = carregar_avisos()
        uid = str(usuario.id)

        if uid not in avisos:
            avisos[uid] = []

        avisos[uid].append({
            "moderador": str(interaction.user),
            "motivo": motivo,
            "data": datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC")
        })
        salvar_avisos(avisos)

        total = len(avisos[uid])
        embed = self.ok(
            "⚠️ Aviso Aplicado",
            f"**Usuário:** {usuario.mention}\n**Motivo:** {motivo}\n"
            f"**Total de avisos:** {total}\n**Mod:** {interaction.user.mention}")
        await interaction.response.send_message(embed=embed)

        try:
            await usuario.send(
                f"⚠️ Você recebeu um aviso em **{interaction.guild.name}**.\n"
                f"**Motivo:** {motivo}\n**Total de avisos:** {total}")
        except Exception:
            pass

    # ── WARNINGS ──────────────────────────────────────────────────────────────
    @app_commands.command(name="warnings", description="Exibe os avisos de um usuário")
    @app_commands.describe(usuario="Usuário")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warnings(self, interaction: discord.Interaction, usuario: discord.Member):
        avisos = carregar_avisos()
        lista = avisos.get(str(usuario.id), [])

        if not lista:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"✅ {usuario.mention} não tem avisos.",
                    color=discord.Color.green()))

        embed = discord.Embed(
            title=f"⚠️ Avisos de {usuario}",
            color=discord.Color.orange())
        for i, a in enumerate(lista, 1):
            embed.add_field(
                name=f"Aviso #{i}",
                value=f"**Motivo:** {a['motivo']}\n**Mod:** {a['moderador']}\n**Data:** {a['data']}",
                inline=False)

        await interaction.response.send_message(embed=embed)

    # ── CLEARWARNS ────────────────────────────────────────────────────────────
    @app_commands.command(name="clearwarns", description="Remove todos os avisos de um usuário")
    @app_commands.describe(usuario="Usuário")
    @app_commands.checks.has_permissions(administrator=True)
    async def clearwarns(self, interaction: discord.Interaction, usuario: discord.Member):
        avisos = carregar_avisos()
        avisos[str(usuario.id)] = []
        salvar_avisos(avisos)
        await interaction.response.send_message(embed=self.ok(
            "✅ Avisos Limpos",
            f"Todos os avisos de {usuario.mention} foram removidos."))

    # ── CLEAR ─────────────────────────────────────────────────────────────────
    @app_commands.command(name="clear", description="Apaga mensagens do canal (máx. 100)")
    @app_commands.describe(quantidade="Quantidade de mensagens")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, quantidade: int):
        if not 1 <= quantidade <= 100:
            return await interaction.response.send_message(
                embed=self.erro("A quantidade deve ser entre 1 e 100."), ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        deletadas = await interaction.channel.purge(limit=quantidade)
        await interaction.followup.send(
            embed=self.ok("🗑️ Mensagens Apagadas", f"**{len(deletadas)}** mensagem(ns) deletada(s)."),
            ephemeral=True)

    # ── SLOWMODE ──────────────────────────────────────────────────────────────
    @app_commands.command(name="slowmode", description="Define o slowmode do canal")
    @app_commands.describe(segundos="Segundos entre mensagens (0 = desativar)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, segundos: int):
        if not 0 <= segundos <= 21600:
            return await interaction.response.send_message(
                embed=self.erro("O valor deve ser entre 0 e 21600 segundos."), ephemeral=True)

        await interaction.channel.edit(slowmode_delay=segundos)
        msg = "Slowmode **desativado**." if segundos == 0 else f"Slowmode definido para **{segundos}s**."
        await interaction.response.send_message(embed=self.ok("🐢 Slowmode", msg))

    # ── LOCK ──────────────────────────────────────────────────────────────────
    @app_commands.command(name="lock", description="Impede que membros enviem mensagens no canal")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        ow = interaction.channel.overwrites_for(interaction.guild.default_role)
        ow.send_messages = False
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=ow)
        await interaction.response.send_message(embed=self.ok(
            "🔒 Canal Travado",
            f"{interaction.channel.mention} foi travado. Membros não podem enviar mensagens."))

    # ── UNLOCK ────────────────────────────────────────────────────────────────
    @app_commands.command(name="unlock", description="Permite que membros enviem mensagens no canal")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        ow = interaction.channel.overwrites_for(interaction.guild.default_role)
        ow.send_messages = True
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=ow)
        await interaction.response.send_message(embed=self.ok(
            "🔓 Canal Destravado",
            f"{interaction.channel.mention} foi destravado."))

    # ── NICK ──────────────────────────────────────────────────────────────────
    @app_commands.command(name="nick", description="Altera o apelido de um usuário")
    @app_commands.describe(usuario="Usuário", apelido="Novo apelido (deixe vazio para remover)")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def nick(self, interaction: discord.Interaction,
                   usuario: discord.Member, apelido: Optional[str] = None):
        await usuario.edit(nick=apelido)
        msg = (f"Apelido de {usuario.mention} alterado para **{apelido}**."
               if apelido else f"Apelido de {usuario.mention} removido.")
        await interaction.response.send_message(embed=self.ok("✏️ Apelido Alterado", msg))

    # ── BANLIST ───────────────────────────────────────────────────────────────
    @app_commands.command(name="banlist", description="Lista os usuários banidos")
    @app_commands.checks.has_permissions(ban_members=True)
    async def banlist(self, interaction: discord.Interaction):
        await interaction.response.defer()
        banidos = [entry async for entry in interaction.guild.bans()]

        if not banidos:
            return await interaction.followup.send(
                embed=discord.Embed(description="Nenhum usuário banido.", color=discord.Color.green()))

        descricao = "\n".join(
            [f"**{e.user}** (`{e.user.id}`) — {e.reason or 'Sem motivo'}"
             for e in banidos[:20]])
        embed = discord.Embed(
            title=f"🔨 Banidos ({len(banidos)})",
            description=descricao,
            color=discord.Color.red())
        if len(banidos) > 20:
            embed.set_footer(text=f"Mostrando 20 de {len(banidos)} banidos.")
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderacao(bot))
