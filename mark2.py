from discord.ext.commands import CommandNotFound
from discord.ext import commands
import discord
import libluci
import os

## default
sample_id = 1798174254  # SARS_CoV-2 sample-id 1798174254
sample_type = "nuccore"  # nucleotide
report_type = "genbank"
doc_type = "html"
## 
soup_validity = True
soup = libluci.soup_collector(str(sample_id), str(sample_type))
#print(soup)

def f(x, soup_, count):
    return {
        "name": libluci.name_collector(soup_),
        "overview": libluci.intro(soup_), 
        "gene": libluci.feature_gene(soup_, count),
        "stem-loop": libluci.feature_stem_loop(soup_, count), 
        "peptide": libluci.feature_peptide(soup_, count), 
        "cds": libluci.feature_cds(soup_, count),
        "source": libluci.feature_source(soup_, count),
        "comment": libluci.comment(soup_),
        "sequence": libluci.chain_sequence(soup_, count),
        "soup": str(soup.text)
    }.get(x, ['Command not found!'])

def h(name, value):
    global sample_type, doc_type, report_type, sample_id
    if name == 'id':sample_id = value
    if name == 'report':report_type = value
    if name == 'doc':doc_type = value
    if name == 'type':sample_type = value
    if name == 'reset':sample_id=1798174254;sample_type="nuccore";report_type="genbank";doc_type="html"


def k(item_name, value, search_type):
    if search_type == 'list':
        if item_name == "gene":
            return libluci.search_id_list(value, "Gene", "Gene", item_name)
        else:
            return libluci.search_id_list(value, item_name.capitalize(), "Sequence", item_name)
    if search_type == 'detail':
        return libluci.search_detail(value, item_name)


def invite_embed():
    embed = discord.Embed(title='MarkII Invite',
                          url='https://discord.com/oauth2/authorize?client_id=798966300448784425&permissions=8&scope=bot',
                          description='Invite MarkII on your server.')
    return embed


def source_embed():
    source_code = 'https://github.com/0x0is1/R.O.C.E-MarkII'
    embed = discord.Embed(title='MarkII Source code',
                          url=source_code,
                          description='Visit MarkII source git.')
    return embed

def help_embed(help_module):
    embed = discord.Embed(title="Rational Operative Communication Entity - Mark II", color=0x03f8fc)
    if help_module == 'default':
        embed.add_field(
        name="Description:", value="This bot is designed for genetic engineering research purpose.", inline=False)
        embed.add_field(
            name="**Commands:**\n", value="`set` : Command used for seting parameters to get data. \n`get` : Command used for getting parameter.\n`search`: command used to make search for genetic materials.\n`option`: command used for getting options saved.\ntype `help <module type>` to get help for specific command.",
            inline=False)
        embed.add_field(
            name="Invite: ", value="get invite link by typing `invite`")
        embed.add_field(
            name="Source: ", value="get source code by typing `source`")
        embed.add_field(
            name="Credits: ", value="get credits info by typing `credits`")
        return embed
    if help_module == 'set':
        embed.add_field(name="**set help**", value="module available for set command.")
        embed.add_field(
            name='Description:', value="use for setting item id and item type.")
        embed.add_field(name='Example: ', value='`set id 1798174254` and `set type nuccore`')
        embed.add_field(name='Options for item type:', value="Nucleotide (`nuccore`)\nGenes (`gene`)\nProtein (`protein`)\nProbe (`probe`)\nPopset(`popset`)")
        embed.add_field(name='Options for item id:', value="use `search <item type> <item name>` to get ids.")
        return embed
    if help_module == 'get':
        embed.add_field(
            name="**get help**", value="module available for get command.")
        embed.add_field(
            name='Description:', value="use for getting data for saved item id and item type.")
        embed.add_field(
            name='Example: ', value='`get gene`, `get cds` etc.')
        embed.add_field(
            name='Options for get:', value="Name (`name`)\nOverview (`overview`)\nComments (`comment`)\nGene (`gene`)\nStem Loop (`stem-loop`)\nPeptide (`peptide`)\nCDS (`cds`)\nSource (`source`)\nAll(`soup`)")
        return embed
    if help_module == 'search':
        embed.add_field(
            name="**search help**", value="module available for search command.")
        embed.add_field(
            name='Description:', value="use for searching data for specific detail type.")
        embed.add_field(
            name='Example: ', value='`search nuccore SARS`, `search gene rept` etc.')
        embed.add_field(
            name='Options for search type:', value="Nucleotide (`nuccore`)\nGenes (`gene`)\nProtein (`protein`)\nProbe (`probe`)\nPopset(`popset`)")
        return embed
    else:
        embed.add_field(name='Unknown mudule', value="Info for given module is not available.")
        return embed

bot = commands.Bot(command_prefix='>')

bot.remove_command('help')

@bot.event
async def on_ready():
    print('Bot is online.')

@bot.command()
async def get(ctx, get_module, count=1):
    if soup_validity and not 'Failed to retrieve sequence' in str(soup):
        current_module = f(get_module, soup, count)
        if type(current_module) == str:
            chunk_len = 1980
            chunks = [current_module[j:j+chunk_len] for j in range(0, len(current_module), chunk_len)]
        else:
            chunks = current_module
        for i in chunks:
            if len(i) > 1980:
                chunks_ = [i[k:k+1980] for k in range(0, len(i), 1980)]
                for l in chunks_:
                    await ctx.send(str('```css\n'+str(l)+'\n```'))
            else:
                await ctx.send(str('```css\n'+str(i)+'\n```'))
    else:
        await ctx.send(soup)

@bot.command()
async def set(ctx, item_name, value):
    h(item_name, value)
    global soup
    global soup_validity
    soup = libluci.soup_collector(str(sample_id), str(sample_type))
    if 'Failed to retrieve sequence' in str(soup):
        soup_validity = False
        await ctx.send(str(soup) + '\nIf you are sure about it, try changing item type.')
    else:
        await ctx.message.add_reaction('✅')

@bot.command()
async def search(ctx, item_name, value, search_type='detail'):
    i = k(item_name, value, search_type)
    chunks_ = [i[k:k+1980] for k in range(0, len(i), 1980)]
    for j in chunks_:
        await ctx.send(str('```css\n'+str(j)+'\n```'))

@bot.command()
async def option(ctx):
    j = 'id: '+ str(sample_id) + '\ntype: ' + sample_type + '\nreport: ' + report_type + '\ndoc: ' + doc_type
    await ctx.send('```css\n'+ j +'\n```')

@bot.command()
async def help(ctx, module='default'):
    await ctx.send(embed=help_embed(module))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('Command not found.')
    else:raise error

@bot.command()
async def ocr(ctx):
    if ctx.message.attachments:
        for i in ctx.message.attachments:
            await ctx.send(libluci.tesseract(i.url))

@bot.command()
async def locate(ctx, ip_address):
    await ctx.send('```json\n' + str(libluci.locate(ip_address)) + '\n```')

token = os.environ.get('EXPERIMENTAL_BOT_TOKEN')
bot.run(token)
