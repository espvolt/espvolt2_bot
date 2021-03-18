import discord
import json

from discord.ext import commands


class Server(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def create_private_channel(self, ctx, name):
        guild = ctx.message.guild
        guild_id = guild.id

        categories = [category.name.lower() for category in guild.categories]

        if not 'private channels' in categories:
            category = await guild.create_category('private channels')

        else:
            for category in guild.categories: # Had to use for loop here instead of discord.util.get('private channels') because some of my friends like capitals even though
                # its uppercase in the view
                if category.name.lower == 'private channels':
                    break
        
        with open('./cogs/private_channels.json', 'r+') as f:
            data = json.load(f)

            if str(guild_id) in data:
                channels = data.get(str(guild_id))

            else:
                channels = {}

            if str(ctx.author.id) in channels:
                return await ctx.send('You already have a private channel')

            channel = await guild.create_voice_channel(name, category=category)

            # no else statement because of return
            channels[str(ctx.author.id)] = str(channel.id) # Need the id for deletion later on

            data[str(guild_id)] = channels

            
            f.seek(0)
            f.truncate(0)
            json.dump(data, f, indent=4)

        # if name == '':
        #     name = '{}\'s private channel'.format(ctx.author.name)

        default_role = guild.default_role
        author_perms = { # Permissions for **kwargs
            'view_channel': True,
            'manage_channels': True,
            'manage_permissions': True,
            'connect': True,
            'speak': True,
            'mute_members': True,
            'deafen_members': True,
            'move_members': True,
            'stream': True
        }

        await ctx.send('Created private channel named {}'.format(name))
        
        await channel.set_permissions(ctx.author, **author_perms)
        await channel.set_permissions(default_role, view_channel=False)

        return


    async def delete_private_channel(self, ctx):
        guild = ctx.message.guild
        guild_id = guild.id

        with open('./cogs/private_channels.json', 'r+') as f:
            data = json.load(f)

            if not str(guild_id) in data:
                return await ctx.send('This server doesn\'t have private channels yet')
            
            if not str(ctx.author.id) in data.get(str(guild_id)):
                return await ctx.send('You don\'t have a voice channel')

            channel_id = data[str(guild_id)].get(str(ctx.author.id)) # Still a string btw

            data[str(guild_id)].pop(str(ctx.author.id))

            f.seek(0)
            f.truncate(0)
            json.dump(data, f, indent=4)

        for category in guild.categories:
            if category.name.lower() == 'private channels':
                break

        channel = discord.utils.get(category.channels, id=int(channel_id))

        await channel.delete()
        return    
        
    @commands.command(aliases=['private'])
    async def priv(self, ctx, operation, *, name=''):
        if operation.lower() in ('create', 'c'):
            if name == '':
                name = '{}\'s private channel'.format(ctx.author.name)

            return await self.create_private_channel(ctx, name)

        elif operation.lower() in ('delete', 'd'):
            return await self.delete_private_channel(ctx)


    async def create_backup(self, ctx):
        channel_list = [] # Used for only channels in categories to find channels not in categories

        guild = ctx.message.guild
        guildID = guild.id

        server_dict = {}
        server_dict['no_category'] = {}

        for category in guild.categories:
            server_dict[category.name] = {}
            for channel in category.channels:
                # test if category has any channels
                channel_dict = {}
                channel_dict['type'] = str(channel.type)
                if channel_dict.get('type') == 'text':
                    channel_dict['nsfw'] = channel.nsfw

                channel_list.append(channel)
                server_dict[category.name][channel.name] = channel_dict

        for channel in guild.channels:
            if not channel in channel_list and channel.name not in server_dict:
                channel_dict = {}
                channel_dict['type'] = str(channel.type)

                if channel_dict.get('type') == 'text':
                    channel_dict['nsfw'] = channel.nsfw

                server_dict['no_category'][channel.name] = channel_dict
        
        with open('./cogs/server_backups.json', 'r+') as f:
            data = json.load(f)

            data[str(guildID)] = server_dict

            f.seek(0)
            f.truncate(0)
            json.dump(data, f, indent=4)


    @commands.command()
    async def backup(self, ctx, revert=''):
        if revert.lower() in ('yes', 'true'):
            pass

        else:
            return await self.create_backup(ctx)
def setup(client):
    client.add_cog(Server(client))

