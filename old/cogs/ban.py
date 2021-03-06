import client
import json
import urllib

import discord
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban naughty memebers of your server"""
        reason = reason or "Reason not provided"

        if member == ctx.author:
            await client.embedSend(ctx,
                                   "Woah, there!",
                                   f"{ctx.author.mention} You cannot ban yourself",
                                   member.avatar_url_as(format=None, static_format='png', size=1024))
            return

        messageok = f"You have been banned from {ctx.guild.name} for {reason}"

        await client.embedSend(ctx, "Good",
                               "Smashed with the Ban Hammer",
                               f"I have banned {member.name} for {reason}",
                               member.avatar_url_as(format=None, static_format='png', size=1024))

        await member.send(messageok)
        await member.ban(reason=reason)
    
    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id):
        """Forgives naughty memebers of your server"""
        member = await self.bot.fetch_user(id)

        link = await ctx.channel.create_invite(max_age=300)
        await ctx.guild.unban(member)

        await client.embedSend(ctx, "Good",
                                "Forgiveness is best",
                                f"I have unbanned {member.name} because they are good",
                                member.avatar_url_as(format=None, static_format='png', size=1024))

        await member.send(f"Hello {member.name}, you have been unbanned from {ctx.guild.name}. Welcome back here's a invite {link}")

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks naughty memebers out of your server"""
        reason = reason or "Reason not provided"

        if member == ctx.author:
            await client.embedSend(ctx, "Error",
                                   "Woah, there!",
                                   f"{ctx.author.mention} You cannot kick yourself",
                                   member.avatar_url_as(format=None, static_format='png', size=1024))
            return

        messageok = f"You have been kicked from {ctx.guild.name} for {reason}"

        await client.embedSend(ctx, "Good",
                               "Kicked out the Server",
                               f"I have banned {member.name} for {reason}",
                               member.avatar_url_as(format=None, static_format='png', size=1024))

        await member.send(messageok)
        await member.kick(reason=reason)

    @ban.error
    async def banError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await client.embedSend(ctx, "Error", "Missing Permissions",
                    f"You are mssing the following permissions: `Ban Members`", None)
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await client.embedSend(ctx, "Error", "Missing Arguments", f"You are mssing the following arguments: `<member>`", None)
            return
    
    @unban.error
    async def unbanError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await client.embedSend(ctx, "Error", "Missing Permissions",
                    f"You are mssing the following permissions: `Ban Members` `Manage Members`", None)
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await client.embedSend(ctx, "Error", "Missing Arguments", f"You are mssing the following arguments: <id>", None)
            return

    @kick.error
    async def kickError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await client.embedSend(ctx, "Error", "Missing Permissions",
                    f"You are mssing the following permissions: `Kick Members`", None)
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await client.embedSend(ctx, "Error", "Missing Arguments", f"You are mssing the following arguments: <member>", None)
            return

def setup(bot):
    bot.add_cog(Ban(bot))
