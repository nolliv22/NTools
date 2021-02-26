import discord
from discord.ext import commands

from subprocess import*
from datetime import datetime

class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lang = {"py" : "py",
                     "ocaml" : "ocaml"}
        self.embed = {"py" : ["Python", 
                                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/768px-Python-logo-notext.svg.png",
                                0x4B8BBE],
                      "ocaml" : ["Ocaml", 
                                "https://ocaml.org/img/colour-icon-170x148.png",
                                0xEA8208]}

    def extension_embed(title="", colour=None):
        e = discord.Embed(title=title, colour=colour, timestamp=datetime.now())
        e.set_footer(text="Eval")
        return e

    def is_codeblock(args):
        return ("```" in args[0]) and ("```" in args[-1])

    def eval_code(self, code, lang):
        p = Popen(self.lang[lang], shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(code.encode("utf-8"))
        return (output or err).decode("latin-1")

    @commands.command(name="eval")
    async def eval_codeblock(self, ctx, lang, *code):
        lang = lang.lower()
        if lang not in self.lang.keys():
            return await ctx.send("Python (!eval py)\nOcaml (!eval ocaml)")
        
        if len(code) != 1:
            return await ctx.send("Ajoutez des apostrophes au début et à la fin du code\nExemple:\n```!eval py 'print(10)'```")
        else:
            code = code[0].replace("'", "")

        output = Eval.eval_code(self, code, lang) or " "

        e = Eval.extension_embed(colour=self.embed[lang][2])
        e.set_author(name=self.embed[lang][0], icon_url=self.embed[lang][1])
        e.add_field(name="Input", value=f"""```{lang}\n{code}```""", inline=False)
        e.add_field(name="Output", value=f"""```{output}```""", inline=False)
        
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Eval(bot))