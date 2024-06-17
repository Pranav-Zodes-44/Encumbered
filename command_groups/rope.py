import discord
from services import user_service, item_service, embed_service, dto,message_service

class RopeCommands(discord.app_commands.Group):
    ...

    bot: discord.Client

    def __init__(self, name, description, bot):
        super(RopeCommands, self).__init__(name=name, description=description)

        self.bot = bot

    
    @discord.app_commands.command(
        name="addrope",
        description="Add rope to your party's inventory"
    )
    async def slash_add_rope(
        self,
        interaction: discord.Interaction,
        length: int,
    ):
        if (length < 1):
            await interaction.response.send_message("Quantity cannot be 0")
            return
        
        user = await user_service.get_or_insert_user(interaction.user.id)
        
        has_party = await user_service.check_user_party(user, interaction)

        if (has_party):

            rope_to_add = dto.ItemDto(
                name = "Rope",
                quantity = length,
            )

            await interaction.response.send_message(f"Adding MORE ROPE to {user.currentParty} (about {length} ft) :inbox_tray:")

            updated_rope = await item_service.add_rope(user.currentParty, rope_to_add)

            embed = embed_service.get_rope_embed(rope_to_add, user, interaction, updated_rope, "add")

            message = await interaction.channel.send(embed=embed)

            await message_service.update_rope(message, user, interaction, updated_rope, rope_to_add.quantity, True, self.bot)


    @discord.app_commands.command(
        name="minusrope",
        description="Remove rope from your party's inventory"
    )
    async def slash_remove_rope(
        self,
        interaction: discord.Interaction,
        length: int,
    ):
        if (length < 1):
            await interaction.response.send_message("Quantity cannot be 0")
            return
        
        user = await user_service.get_or_insert_user(interaction.user.id)
        
        has_party = await user_service.check_user_party(user, interaction)

        if (has_party):

            rope_to_remove = dto.ItemDto(
                name = "Rope",
                quantity = length,
            )

            await interaction.response.send_message(f"Using some rope from {user.currentParty}'s stash (about {length} ft) :outbox_tray:")

            updated_rope, error = await item_service.remove_rope(user.currentParty, rope_to_remove)

            embed = embed_service.get_rope_embed(rope_to_remove, user, interaction, updated_rope, "remove")

            if (updated_rope is None):
                await interaction.channel.send(content=error)

            message = await interaction.channel.send(embed=embed)

            await message_service.update_rope(message, user, interaction, updated_rope, rope_to_remove.quantity, False, self.bot)


    @discord.app_commands.command(
        name="getrope",
        description="Get the amount of rope the party collectively has"
    )
    async def slash_get_rope(
        self,
        interaction: discord.Interaction
    ):
        user = await user_service.get_or_insert_user(interaction.user.id)
        
        has_party = await user_service.check_user_party(user, interaction)

        if (has_party):
            await interaction.response.send_message(f"Getting {user.currentParty}'s rope collection...")

            rope = await item_service.get_item(user.currentParty, "Rope")

            if (rope is None):
                await interaction.channel.send(content="Seems like there's no rope... :( Use /addrope to add some to the stash")
                return
            
            await interaction.channel.send(embed=embed_service.get_rope_embed(rope, user, interaction))
