import discord
from discord.ext import commands,tasks
import random
import asyncio
import time


client = commands.Bot(command_prefix="^")#Change your prefix here
client.remove_command("help")

@client.event
async def on_ready():
    print("Bot is ready")
    await client.change_presence(activity=discord.Game(name='Develop by DeepKungChannel'))



player1 = ""
player2 = ""
turn = ""
numturn = 0
count_render = 0
board_render = []
board = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]
]
gameOver = True
modes = 1

@client.command(aliases=['connect'])
async def connectfour(ctx,p1:discord.Member,p2:discord.Member):
    global player1
    global player2
    global gameOver
    global turn
    global modes

    if gameOver:
        global board
        global numturn
        board = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]
        player1 = p1.name
        player2 = p2.name

        board_render = []
        count_render = 0
        num = random.randint(1,2)
        if num == 1:
            numturn = 1
            turn = player1
        elif num == 2:
            numturn = 2
            turn = player2
        for count, i in enumerate(board):
            if ([0, 0, 0, 0, 0, 0, 0, 0]== i) and count_render <= 3:
                count_render +=1
                board_render.append(i)
            elif count_render <= 3:
                board_render.append(i)
            
        board_render.reverse()
        await ctx.send(render(board_render))
        await ctx.send("{} Turn!".format(turn))
        board_render.reverse()
        gameOver = False
    else:
        await ctx.send("Game is already start.")
    
        
@client.command(aliases=['p'])
async def place(ctx,num:int):
    global player1
    global player2
    global gameOver
    global turn
    global modes

    if not gameOver:
        global board
        global numturn

        counts = 0
        count_render = 0
        board_render = []
        count_tie = 0
        if turn == ctx.author.name:
            for count, i in enumerate(board):
                if ([0, 0, 0, 0, 0, 0, 0, 0]== i) and count_render <= 3:
                    count_render +=1
                    board_render.append(i)
                elif count_render <= 3:
                    board_render.append(i)
            for count, i in enumerate(board):
                if i[num-1] == 0:
                    counts += 1
                    board[count][num-1] = numturn
                    win = windetect(board,turn)
                    if win:
                        board_render.reverse()
                        line = ''
                        await ctx.send(render(board_render))
                        gameOver = True
                            # time.sleep(0.3)
                        await ctx.send("{} win!".format(turn))
                        await ctx.send(":partying_face: Congratulations!")
                        board_render.reverse()
                        return
                    if turn == player1:
                        numturn= 2
                        turn = player2
                    else:
                        numturn = 1
                        turn = player1
                    board_render.reverse()
                    for i in board:
                        print(i)
                    line = ''
                    await ctx.send(render(board_render))
                    await ctx.send("{} Turn!".format(turn))
                    print("{} Turn!".format(turn))
                    print()
                    board_render.reverse()
                    return
                for y in i:
                    if y == 0:
                        count_tie += 1
                if count_tie == 0:
                    counts += 1
                    if modes == 1:
                        await ctx.send(render(board_render))
                    elif modes == 2:
                        await ctx.send(embed=render(board_render))
                    await ctx.send("Tie!")
                    return
        else:
            await ctx.send("It's not your turn")
            counts += 1
        if counts == 0:
            await ctx.send("Column is full please select anothor column.")
    else:
        await ctx.send("Please start with .connectfour command.")

def render(board_render):
    line=''
    global modes
    for count,x in enumerate(board_render):
        for y in x:
            if y == 0:
                line += (":white_medium_square:" + ' ')
            elif y == 1:
                line += (":red_circle:" + ' ')
            elif y == 2:
                line += (":yellow_circle:" + ' ')
        if count <= len(board_render)-2:
            line += "\n"
    if modes == 1:
        return line
    elif modes == 2:
        embed = discord.Embed(title="Connect 4 Game",color=discord.Color.green())
        embed.add_field(name='Display',value=line)
        return embed


def windetect(board,turn):
    global numturn
    boardHeight = len(board)
    boardWidth = len(board[0])
    tile = numturn

    # check horizontal spaces
    for y in range(boardHeight):
        for x in range(boardWidth - 3):
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                return True
    
    # check vertical spaces
    for x in range(boardWidth):
        for y in range(boardHeight - 3):
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                return True
    
    # check / diagonal spaces
    for x in range(boardWidth - 3):
        for y in range(3, boardHeight):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                return True

    # check \ diagonal spaces
    for x in range(boardWidth - 3):
        for y in range(boardHeight - 3):
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                return True
    return False   

@client.command()
async def stop(ctx):
    global gameOver
    if not gameOver:
        gameOver = True
        await ctx.send("The Game is stop.")
        print("The Game is stop.")
    else:
        await ctx.send("The Game has stopped")
        print("The Game has stopped")


@mode.error
async def mode_error(ctx,error):
    text = "Mode:\n    1. print a game in text\n    2. print a game in embed format"
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(text)

@client.command()
async def help(ctx):
    embed = discord.Embed(title='Help',color=discord.Color.green())
    embed.add_field(name="Connectfour",value='Start this game (Use: ^connectfour @member#1010 @member#0101)',inline=False)
    embed.add_field(name='Place',value='Place 1-8 column')
    embed.add_field(name='Stop',value='Stop this game')
    await ctx.send(embed=embed)

client.run("-----Your Bot Token-----")