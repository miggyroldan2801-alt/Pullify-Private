import discord

class EmbedFactory:
    """Standardized factory for generating system-branded embeds."""
    
    COLOR_PRIMARY = discord.Color.blue()
    COLOR_SUCCESS = discord.Color.green()
    COLOR_ERROR = discord.Color.red()
    COLOR_WARNING = discord.Color.gold()

    @staticmethod
    def create_embed(title: str, description: str, color: discord.Color = COLOR_PRIMARY) -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )
        embed.set_footer(text="PULLIFY-UTILS // SECURE_OPERATIONAL_SUPPORT")
        return embed

    @classmethod
    def ticket_embed(cls, user: discord.Member, reason: str) -> discord.Embed:
        embed = cls.create_embed("Support Ticket", "A new support request has been initiated.", cls.COLOR_PRIMARY)
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        return embed

    @classmethod
    def error_embed(cls, error_msg: str) -> discord.Embed:
        return cls.create_embed("System Error", error_msg, cls.COLOR_ERROR)