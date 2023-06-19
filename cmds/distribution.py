import discord
from discord.ext import commands
import json
from core.classes import Cog_Extension
import random

with open ("background_setting.json",'r',encoding="utf8") as jfile:
    jdata=json.load(jfile)

class distribution(Cog_Extension):
    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.content.endswith("是南家") and self.game_process == "distribute" and msg.author==self.bot.user:
            print("OK")
            with open ("background_setting.json",'r',encoding="utf8") as jfile:
                jdata=json.load(jfile)
            player_num = 'ESWN'  #ESWN

            for i in range(4):
                cards=random.sample(jdata["poker"],k=13)#重新打散牌
                sort_list=[]
                for element in cards: 
                    jdata["poker"].remove(element)
                    sort_list.append(jdata["sort normal"][element])
                sort_list.sort()

                for a in range(13): cards[a]=jdata["sort_back normal"][str(sort_list[a])]
                jdata[F"player{player_num[i]}_cards"]=cards
                with open("background_setting.json",'w',encoding="utf8")as jfile:
                    json.dump(jdata,jfile,indent=4)

            for i in range(4):
                message=''
                for card in jdata[F"player{player_num[i]}_cards"]: message+=F"{card},"
                user=await self.bot.fetch_user(jdata["player"][i])
                text=await user.send(message)
                jdata[F"player{player_num[i]}_id"]=text.id
                with open("background_setting.json",'w',encoding="utf8")as jfile:
                    json.dump(jdata,jfile,indent=4)
                print(jdata[F"player{player_num[i]}_id"])

            Cog_Extension.getcard=True
            Cog_Extension.startplaying=True
            print ("OK")

            for init_color in ["club","diamond","heart","space"]:
                for init_num in ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]:           
                    jdata["poker"].append(F"{init_color} {init_num}")
            
            
            with open("background_setting.json",'w',encoding="utf8")as jfile:
                json.dump(jdata,jfile,indent=4)
            print(self.join)
            self.join=True
            with open("background_setting.json",'w',encoding="utf8")as jfile:
                json.dump(jdata,jfile,indent=4)
            jdata["game_process"] = "setking"


def setup(bot):
    bot.add_cog(distribution(bot))