import discord
from discord.ext import commands
import json
from discord.ext.commands.cog import Cog
from core.classes import Cog_Extension
import random

with open ("background_setting.json",'r',encoding="utf8") as jfile:
    jdata=json.load(jfile)

class king(Cog_Extension):
    @commands.command()#待做:1.改成贏敦的人先出 2.出過的牌削掉 3.判斷遊戲輸贏 4.玩家超過五人 5.奇怪訊息處理
    async def setking(self,ctx,line:int,king_color,team,win_player:str):
        #初始設定
        with open ("background_setting.json",'r',encoding="utf8") as jfile:
                jdata=json.load(jfile)
        if jdata["game_process"] == "setking":
            player_num = "ESWN"
            with open ("background_setting.json",'r',encoding="utf8") as jfile:
                jdata=json.load(jfile)

            self.team=team
            self.king_color=king_color
            for i in player_num:
                if win_player == i:
                    self.counter = i-2
            if win_player <=1:
                jdata["dream"] = win_player+2
            elif 2 <=win_player <=3:
                jdata["dream"] = win_player-2
            with open("background_setting.json",'w',encoding="utf8")as jfile:
                json.dump(jdata,jfile,indent=4)
            


            if self.king_color in jdata["color"] and 1<=line<=7 and (self.team=="EW" or self.team=="NS"):
                if self.team=="EW":
                    self.EW_win_edition=line+6
                    self.NS_win_edition=14-self.EW_win_edition
                    await ctx.channel.send(F"王牌花色是{self.king_color}\n東西家要拿{self.EW_win_edition}墩，南北家要拿{self.NS_win_edition}墩")
                
                elif self.team=="NS":
                    self.NS_win_edition=line+6
                    self.EW_win_edition=14-self.NS_win_edition
                    await ctx.channel.send(F"王牌花色是{self.king_color}\n東西家要拿{self.EW_win_edition}墩，南北家要拿{self.NS_win_edition}墩")
                
                
                if self.king_color=="Middle" or self.king_color=="mini":
                    for i in range(4):
                        with open ("background_setting.json",'r',encoding="utf8") as jfile:
                            jdata=json.load(jfile)
                        sort_list=[]
                        for element in jdata[F"player{player_num[i]}_cards"]:  sort_list.append(jdata[F"sort {self.king_color}"][element])
                        sort_list.sort()
                        for a in range(13): jdata[F"player{player_num[i]}_cards"][a]=jdata[F"sort_back {self.king_color}"][str(sort_list[a])]
                        with open("background_setting.json",'w',encoding="utf8")as jfile:
                            json.dump(jdata,jfile,indent=4)

                        message=''
                        for card in jdata[F"player{player_num[i]}_cards"]: message+=F"{card},"
                        user=await self.bot.fetch_user(jdata["player"][player_num[i]])
                        delete=await user.fetch_message(jdata[F"player{player_num[i]}_id"])
                        await delete.delete()
                        text=await user.send(message)
                        jdata[F"player{player_num[i]}_id"]=text.id
                        with open("background_setting.json",'w',encoding="utf8")as jfile:
                            json.dump(jdata,jfile,indent=4)
                
                self.channel=ctx.channel
                self.EW_wincount,self.NS_wincount=0,0
                self.cards=[]
                jdata["game_process"] = "playing"
            else : await ctx.channel.send("你真的要這樣打牌嗎?")