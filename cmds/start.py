import discord
from discord.ext import commands
import json
from core.classes import Cog_Extension


with open ("background_setting.json",'r',encoding="utf8") as jfile:
    jdata=json.load(jfile)

class start(Cog_Extension):
    def compare(list):
        a=0
        for i in range(4):
            if list[i]>a: 
                a=list[i] 
                max=i 
        return max
    
    def judge(self,card,player):
        number=[]
        if self.king_color=="NK": 
            king_for_this_round=card[0][:-2]
            for i in range(4):
                if card[i][:-2]!=king_for_this_round:
                    number.append[0]
                else: number.append[jdata["No King"][card[-1]]]
            winner=player[self.compare(number)]
            return winner
        elif self.king_color=="mn":
            king_for_this_round=card[0][:-2]
            for i in range(4):
                if card[i][:-2]!=king_for_this_round:
                    number.append[0]
                else: number.append[jdata["mini"][card[-1]]]
            winner=player[self.compare(number)]
            return winner
        elif self.king_color=="Md":
            king_for_this_round=card[0][:-2]
            for i in range(4):
                if card[i][:-2]!=king_for_this_round:
                    number.append[0]
                else: number.append[jdata["Medium"][card[-1]]]
            winner=player[self.compare(number)]
            return winner
        else:
            king_for_this_round=card[0][:-2]
            for i in range(4):
                if card[i][:-2]==self.king_color:
                    number.append[jdata["normal"][card[-1]+13]]
                elif card[i][:-2]!=king_for_this_round:
                    number.append[0]
                else: number.append[jdata["normal"][card[-1]]]
            winner=player[self.compare(number)]
            return winner
        
    @commands.Cog.listener()
    async def game(self):
        a_wincount,b_wincount=0,0
        while a_wincount<self.a_win_editon or b_wincount<self.b_win_edition:
            self.cards=[]
            for self.counter in range(4):
                @commands.Cog.listener()
                async def on_message(self,msg):
                    if msg.content in jdata["poker"] and msg.author==self.player[self.counter]:
                        self.cards+=msg.content
                    else: self.counter-=1
            win=self.judge(self.cards,self.player)
            if win in self.ateam:a_wincount+=1
            else: b_wincount+=1
            await self.channel.send(F"{win}贏了這一墩\n目前a隊拿了{a_wincount}墩，還要拿{self.a_win_edition-a_wincount}\n目前b隊拿了{b_wincount}墩，還要拿{self.a_win_edition-a_wincount}")
            

    




def setup(bot):
    bot.add_cog(start(bot))