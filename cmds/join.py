import discord
from discord.ext import commands
import json
from core.classes import Cog_Extension
from cmds.distribution import distribution
import random
with open ("background_setting.json",'r',encoding="utf8") as jfile:
    jdata=json.load(jfile)
    
class people(Cog_Extension):
    @commands.Cog.listener()  #參加遊戲的指令
    async def on_message(self,msg):
        with open ("background_setting.json",'r',encoding="utf8") as jfile:
            jdata=json.load(jfile)
        if jdata["game_process"]=="join":  #參加遊戲指令的開關

            if msg.content == "打橋牌":#如果輸入訊息為{打橋牌}，就把傳訊息的人id加進json的player
                #if msg.auther.id not in jdata["bridge_player"]:
                    
                    jdata["bridge_player"].append(msg.author.id)
                    self.bridge_people+=1
                    print(self.bridge_people)
                    with open("background_setting.json",'w',encoding="utf8")as jfile:
                        json.dump(jdata,jfile,indent=4)
                    await msg.channel.send(F"目前有{self.bridge_people}人玩橋牌") 


                    if self.bridge_people==4:  #玩家滿四個人後，將玩家隨機排列，再將第一、二個人定為EW組，第三、四個人為NS組
                        jdata["bridge_player"]=random.sample(jdata["bridge_player"],k=4)
                        with open("background_setting.json",'w',encoding="utf8")as jfile:
                            json.dump(jdata,jfile,indent=4)

                        team_EW=""
                        team_NS=""
                        for i in range(4):
                            user=await self.bot.fetch_user(jdata["bridge_player"][i])

                            if i/2 == 0:
                                team_EW+=F"{user} "
                            elif i/2 !=0:
                                team_NS+=F"{user} "

                        player_list = jdata["bridge_player"]
                        await msg.channel.send(F"      {player_list[3]}是北家      ")
                        await msg.channel.send(F"{player_list[2]}是西家   {player_list[0]}是東家")
                        await msg.channel.send(F"      {player_list[1]}是南家      ")
                        #jdata["player"][1],jdata["player"][2]=jdata["player"][2],jdata["player"][1]
                        with open ("background_setting.json",'r',encoding="utf8") as jfile:
                            jdata=json.load(jfile)
                        jdata["game_process"]="distribute"
                        jdata["game_mode"] = "bridge"
                        with open("background_setting.json",'w',encoding="utf8")as jfile:
                            json.dump(jdata,jfile,indent=4)

                    elif self.bridge_people>=5:
                        jdata["bridge_player"]=[]
                        jdata["game_process"]= "join"
                        with open("background_setting.json",'w',encoding="utf8")as jfile:
                            json.dump(jdata,jfile,indent=4)                        
                        await msg.channel.send("超過四人，發生錯誤\n將人數歸零，重新開始")

            if msg.content == "打加咩":#如果輸入訊息為{打加咩}，就把傳訊息的人id加進json的player
                    jdata["jm_player"].append(msg.author.id)
                    self.jm_people+=1
                    with open("background_setting.json",'w',encoding="utf8")as jfile:
                        json.dump(jdata,jfile,indent=4)
                    await msg.channel.send(F"目前有{self.jm_people}人玩加咩") 

                    if self.jm_people==4:  #玩家滿四個人後，將玩家隨機排列，再將第一、二個人定為EW組，第三、四個人為NS組
                        jdata["jm_player"]=random.sample(jdata["jm_player"],k=4)
                        with open("background_setting.json",'w',encoding="utf8")as jfile:
                            json.dump(jdata,jfile,indent=4)

                        player_list = jdata["jm_player"]
                        await msg.channel.send(F"      {player_list[3]}是北家      ")
                        await msg.channel.send(F"{player_list[2]}是西家   {player_list[0]}是東家")
                        await msg.channel.send(F"      {player_list[1]}是南家      ")
                        #jdata["player"][1],jdata["player"][2]=jdata["player"][2],jdata["player"][1]
                        with open ("background_setting.json",'r',encoding="utf8") as jfile:
                            jdata=json.load(jfile)
                        jdata["game_process"]="distribute"
                        jdata["game_mode"] = "jm"
                        with open("background_setting.json",'w',encoding="utf8")as jfile:
                            json.dump(jdata,jfile,indent=4)

                    elif self.jm_people>=5:
                        jdata["jm_player"]=[]
                        jdata["game_process"]= "join"
                        with open("background_setting.json",'w',encoding="utf8")as jfile:
                            json.dump(jdata,jfile,indent=4)                        
                        await msg.channel.send("超過四人，發生錯誤\n將人數歸零，重新開始")

            elif msg.content=="不打橋牌了":  #若輸入{不打橋牌了}，則把此玩家id從bridge_player中移除
                if msg.author.id in jdata["bridge_player"]:
                    jdata["bridge_player"].remove(msg.author.id)
                    self.bridge_people-=1
                    with open("background_setting.json",'w',encoding="utf8") as jfile:
                        json.dump(jdata,jfile,indent=4)
                    await msg.channel.send(F"目前有{self.bridge_people}人玩橋牌")
                else:
                    await msg.channel.send("沒有要打橋牌是怎麼不打的啦(怒")

            elif msg.content=="不打加咩了":  #若輸入{不打加咩了}，則把此玩家id從jm_player中移除
                if msg.author.id in jdata["jm_player"]:
                    jdata["jm_player"].remove(msg.author.id)
                    self.jm_people-=1
                    with open("background_setting.json",'w',encoding="utf8") as jfile:
                        json.dump(jdata,jfile,indent=4)
                    await msg.channel.send(F"目前有{self.jm_people}人玩加咩")
                else:
                    await msg.channel.send("沒有要打加咩是怎麼不打的啦(怒")
            

    @commands.command()
    async def use(self,ctx):
        await ctx.send('''橋牌機器人使用說明:
        1.輸入(來打牌)，機器人會登錄玩家；輸入(不打了)，則可以取消登錄
        2.湊滿4個人時，會將玩家隨機分為東西家(EW)與南北家(NS)，左上、左下、右上、右下編號分別為E、S、W、N(出牌順序)
        3.喊牌時以在語音群以出牌方向進行，喊完牌後用([setking 喊的線位 王牌花色 隊伍 喊到王的玩家編號)的形式輸入
        花色:(mini),club,diamond,(Middle),heart,space,No_King
        ex:[setking 3 No_King NS 2(注意每項輸入間有空格)
        4.出牌方式為在頻道上把自己要打的牌用訊息送出''')

        #await ctx.send("""橋牌機器人使用說明:
        #1.輸入(來打牌)，機器人會登錄玩家；輸入(不打了)，則可以取消登錄
        #2.湊滿4個人時，會將玩家隨機分為東西家(EW)與南北家(NS)，左上、左下、右上、右下編號分別為E、S、W、N(出牌順序)  
        #3.喊牌時以在語音群以出牌方向進行，喊完牌後用([setking 喊的線位 王牌花色 隊伍 喊到王的玩家編號)的形式輸入
        #花色:mini,club,diamond,Middle,heart,space,No_King
        #ex:[set 3 No_King b 2(注意每項輸入間有空格)
        #4.出牌方式為在頻道上把自己要打的牌用訊息送出""")
async def setup(bot):
    await bot.add_cog(people(bot))