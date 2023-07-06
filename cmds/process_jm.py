import discord
from discord.ext import commands
import json
from discord.ext.commands.cog import Cog
from core.classes import Cog_Extension
import random
import time


class process_jm(Cog_Extension):
    def compare(self,list):#傳入list後，挑出其中最大數字的引數
        a=0
        max=0
        for i in range(4):
            if list[i]>a: 
                a=list[i] 
                max=i 
        return max

    def judge(self,card:list):
        each_color = []
        each_number = []
        if card[0][-2:]=="10":#10則取到倒數第3
            round_color= card[i][:-3]#第一張為墩的主花色
        else:   
            round_color = card[0][:-2]

        for i in range(4):#取數字及花色
            if card[i][-2:]=="10":#10取到倒數3
                each_number[i].append(10)
                each_color.append(card[i][:-3])
            elif card[i][-1] == 'J':
                each_number[i].append(11)
                each_color.append(card[i][:-2])
            elif card[i][-1] == 'Q':
                each_number[i].append(12)
                each_color.append(card[i][:-2])
            elif card[i][-1] == 'K':
                each_number[i].append(13)
                each_color.append(card[i][:-2])
            elif card[i][-1] == 'A':
                each_number[i].append(14)
                each_color.append(card[i][:-2])    
            else:
                each_number[i] = card[i][-1]#其他取到倒數2
                each_color.append(card[i][:-2])

        for i in range(4):#判斷花色
            temp_color = each_color[i]
            if self.king =='No_King':#特殊情況(無王牌)
                if temp_color != round_color:
                    each_number[i] = 0
            if self.king =='mini':
                if temp_color != round_color:
                    each_number[i] = 0
                else:
                    each_number[i] = 15-each_number[i]
            if self.king =='Middle':
                if temp_color != round_color:
                    each_number[i] = 0.
                else:
                    each_number[i] = 36-(each_number[i]-8)**2 + each_number[i]/14
            else:#有王牌
                if temp_color == self.king_color:
                    each_number[i] += 13
                elif temp_color != self.king_color or temp_color != round_color:
                    each_number[i] = 0
        win=process_jm.compare(self,each_number)
        return win


    @commands.Cog.listener()
    async def on_message(self,msg):
        player_num = "ESWN"
        player_num_cn = "東南西北"


        with open ("background_setting.json",'r',encoding="utf8") as jfile:  #order: 2301 1230
            jdata=json.load(jfile)
        if jdata["game_process"]=="playing_jm" and msg.author!=self.bot.user:
            self.counter += 1
            if self.counter == 4:   self.counter -= 4
            player=await self.bot.fetch_user(jdata["player"][self.counter])
            if msg.content in jdata["poker"] and msg.author == player:
                if msg.content in jdata[F"player{player_num[self.counter]}_cards"]:
                    content=msg.content
                    self.cards.append(content)
                    jdata[F"player{player_num[self.counter]}_cards"].remove(content)
                    with open("background_setting.json",'w',encoding="utf8")as jfile:
                        json.dump(jdata,jfile,indent=4)
                    if len(self.cards)!=4: #還沒出完
                        if self.counter == 3 :self.counter -= 4
                        await msg.channel.send(F"輪到{player_num_cn[self.counter+1]}家出牌")#下一個人
                        time.sleep(0.2)
                else: 
                    await msg.channel.send("你要不要看看你都打了什麼")
                    self.counter-=1 #回到原本的人
            else : self.counter-=1

            
            if len(self.cards)==4:#出完一輪
                trick_win=process_jm.judge(self,self.cards)
                trick_win-=(self.counter+1) #回推贏家(card是照出牌順序排列)
                if trick_win<=-1: trick_win+=4
                jdata["win_trick"][trick_win] += 1#贏的加1
                winner=await self.bot.fetch_user(jdata["player"][trick_win])
                await self.channel.send(F'{winner}贏了這一墩  目前墩數\n   北家:{jdata["win_trick"][3]}/{jdata["call_trick"][3]}\n西家:{jdata["win_trick"][2]}/{jdata["call_trick"][2]}     東家:{jdata["win_trick"][0]}/{jdata["call_trick"][0]}\n   南家:{jdata["win_trick"][1]}/{jdata["call_trick"][1]}\n') 
                await self.channel.send(F"輪到{player_num_cn[trick_win]}家出牌")
                self.trickcount += 1
                with open("background_setting.json",'w',encoding="utf8")as jfile:
                    json.dump(jdata,jfile,indent=4)
                    
                #重置
                self.cards=[]
                self.counter=trick_win-1#跑下一次會再加1

                #結束
                if self.trickcount == 13:
                    await self.channel.send("遊戲結束，東西家勝利")
                    jdata["player"]=[]
                    for i in range(4):
                        jdata[F"player{player_num[i]}_cards"]=[]
                    jdata["join"]="True"
                    with open("background_setting.json",'w',encoding="utf8")as jfile:
                        json.dump(jdata,jfile,indent=4)
                    self.count_win=False
                    self.set_people = 0
                    self.trickcount = 0
                
                #下一墩準備
                else:
                    for i in range(4):
                        with open ("background_setting.json",'r',encoding="utf8") as jfile:#載入出牌後各家牌
                            jdata=json.load(jfile)
                        message=''
                        for card in jdata[F"player{player_num[i]}_cards"]: message+=F"{card},"
                        user=await self.bot.fetch_user(jdata["player"][i])
                        delete=await user.fetch_message(jdata[F"player{player_num[i]}_id"])
                        await delete.delete()
                        text=await user.send(message)
                        jdata[F"player{player_num[i]}_id"]=text.id
                        with open("background_setting.json",'w',encoding="utf8")as jfile:
                            json.dump(jdata,jfile,indent=4)

async def setup(bot):
    await bot.add_cog(process_jm(bot)) 