"""NetSpeed cog for Red-DiscordBot by PhasecoreX."""
import asyncio
import concurrent

import discord
import speedtest
from redbot.core import checks, commands


class NetSpeed(commands.Cog):
    """Test your servers internet speed."""

    @commands.command(aliases=["speedtest"])
    @checks.is_owner()
    async def netspeed(self, ctx):
        """Measure your internet speed."""
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        loop = asyncio.get_event_loop()
        s = speedtest.Speedtest(secure=True)
        the_embed = await ctx.send(embed=self.generate_embed(0, s.results.dict()))
        await loop.run_in_executor(executor, s.get_servers)
        await loop.run_in_executor(executor, s.get_best_server)
        await the_embed.edit(embed=self.generate_embed(1, s.results.dict()))
        await loop.run_in_executor(executor, s.download)
        await the_embed.edit(embed=self.generate_embed(2, s.results.dict()))
        await loop.run_in_executor(executor, s.upload)
        await the_embed.edit(embed=self.generate_embed(3, s.results.dict()))

    @staticmethod
    def generate_embed(step: int, results_dict):
        """Generate the embed."""
        measuring = ":mag: Measuring..."
        waiting = ":hourglass: Waiting..."

        color = discord.Color.red()
        title = "Measuring internet speed..."
        message_ping = measuring
        message_down = waiting
        message_up = waiting
        if step > 0:
            message_ping = "**{}** ms".format(results_dict["ping"])
            message_down = measuring
        if step > 1:
            message_down = "**{:.2f}** mbps".format(
                results_dict["download"] / 1_000_000
            )
            message_up = measuring
        if step > 2:
            message_up = "**{:.2f}** mbps".format(results_dict["upload"] / 1_000_000)
            title = "NetSpeed Results"
            color = discord.Color.green()
        embed = discord.Embed(title=title, color=color)
        embed.add_field(name="Ping", value=message_ping)
        embed.add_field(name="Download", value=message_down)
        embed.add_field(name="Upload", value=message_up)
        return embed
