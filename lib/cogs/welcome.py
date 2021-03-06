from discord import Forbidden, Embed
from discord.ext.commands import Cog
from discord.ext.commands import command

from ..db import db

class Welcome(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("welcome")

	@Cog.listener()
	async def on_guild_join(self, ctx, guild):
		db.execute("INSERT INTO guilds (GuildID) VALUES (?)", guild.id)
		try:

			await ctx.send(embed=Embed(description=f"Hello {ctx.guild.name}!\n Type op.help to get started."))

		except:
			pass

	@Cog.listener()
	async def on_member_join(self, member):
		try:
			db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
			await self.bot.get_channel(761766201247793163).send(f"{member.mention} has checked into **{member.guild.name}**")

		except Forbidden:
			pass

		try:
			await member.send("Subcribe to Elevator Operator\n https://www.youtube.com/channel/UC-E4Tpi9nVMIH-S_cJcoPIQ")

		except Forbidden:
			pass

		try:
			await member.add_roles(member.guild.get_role(788562239958810635))

		except:
			pass


	@Cog.listener()
	async def  on_member_remove(self, member):
		db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
		try:
			await self.bot.get_channel(788516956285435904).send(f"{member.display_name} has checked out of **{member.guild.name}**")

		except Forbidden:
			pass

def setup(bot):
	bot.add_cog(Welcome(bot))