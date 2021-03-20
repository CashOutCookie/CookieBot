import discord, re, asyncio, logging, random, typing, json, os
from functools import partial
from discord.ext import commands
from dataclasses import dataclass
from aiohttp import request

log = logging.getLogger(__name__)


@dataclass
class Square:
    cookie: typing.Optional[str]
    aimed: bool

Grid = typing.List[typing.List[Square]]
EmojiSet = typing.Dict[typing.Tuple[bool, bool], str]

@dataclass
class Player:
    user: discord.Member
    board: discord.Message
    opponent_board: discord.Message
    grid: Grid

COOKIES = {
    "Cookie": 5,
    "Choco-Chip Cookie": 2,
}

COOKIE_EMOJIS = {
    (True, True): ":fire:",
    (True, False): ":cookie:",
    (False, True): ":anger:",
    (False, False): ":milk:",
}
HIDDEN_EMOJIS = {
    (True, True): ":partying_face:",
    (True, False): ":black_circle:",
    (False, True): ":white_circle:",
    (False, False): ":black_circle:",
}
LETTERS = (
    ":stop_button::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d:"
    ":regional_indicator_e:"
)
NUMBERS = [
    ":one:",
    ":two:",
    ":three:",
    ":four:",
    ":five:",
]
CANCEL = "<a:cancel:810688215962746930>"
ACCEPT = "<a:accept:810685283033022485>"

class Game:
    def __init__(
        self,
        bot: commands.Bot,
        channel: discord.TextChannel,
        player1: discord.Member,
        player2: discord.Member
    ) -> None:

        self.bot = bot
        self.public_channel = channel

        self.p1 = Player(player1, None, None, self.generate_grid())
        self.p2 = Player(player2, None, None, self.generate_grid())

        self.gameover: bool = False

        self.turn: typing.Optional[discord.Member] = None
        self.next: typing.Optional[discord.Member] = None

        self.match: typing.Optional[typing.Match] = None
        self.surrender: bool = False

        self.setup_grids()

    @staticmethod
    def generate_grid() -> Grid:
        return [[Square(None, False) for _ in range(5)] for _ in range(5)]

    @staticmethod
    def format_grid(player: Player, emojiset: EmojiSet) -> str:
        grid = [
            [emojiset[bool(square.cookie), square.aimed] for square in row]
            for row in player.grid
        ]

        rows = ["".join([number] + row) for number, row in zip(NUMBERS, grid)]
        return "\n".join([LETTERS] + rows)

    @staticmethod
    def get_square(grid: Grid, square: str) -> Square:
        index = ord(square[0].upper()) - ord("A")
        number = int(square[1:])

        return grid[number-1][index]  # -1 since lists are indexed from 0

    async def game_over(
        self,
        *,
        winner: discord.Member,
        loser: discord.Member
    ) -> None:
        await self.public_channel.send(f"Game Over, {winner.mention} won against {loser.mention} and earned 200 cookies")
        AWARD_API = os.environ.get('AWARD_API')
        for i in self.bot.listcookies:
            if i[1] == winner.id:
                winnername = i[0]
        data = {"username":winnername, "amount": "200"}
        credentials = json.dumps(data)
        async with request("POST", AWARD_API, data=credentials, headers={'Content-type':'application/json', 'Accept':'application/json'}) as response:
            pass

        for player in (self.p1, self.p2):
            grid = self.format_grid(player, COOKIE_EMOJIS)
            await self.public_channel.send(f"{player.user}'s Board:\n{grid}")

    @staticmethod
    def check_sink(grid: Grid, cookie: str) -> bool:
        return all(square.aimed for row in grid for square in row if square.cookie == cookie)

    @staticmethod
    def check_gameover(grid: Grid) -> bool:
        return all(square.aimed for row in grid for square in row if square.cookie)

    def setup_grids(self) -> None:
        for player in (self.p1, self.p2):
            for name, size in COOKIES.items():
                while True:  # Repeats if about to overwrite another cookie
                    ship_collision = False
                    coords = []

                    coord1 = random.randint(0, 4)
                    coord2 = random.randint(0, 5 - size)

                    if random.choice((True, False)):  # Vertical or Horizontal
                        x, y = coord1, coord2
                        xincr, yincr = 0, 1
                    else:
                        x, y = coord2, coord1
                        xincr, yincr = 1, 0

                    for i in range(size):
                        new_x = x + (xincr * i)
                        new_y = y + (yincr * i)
                        if player.grid[new_x][new_y].cookie:  # Check if there's already a cookie
                            ship_collision = True
                            break
                        coords.append((new_x, new_y))
                    if not ship_collision:  # If not overwriting any other cookie spaces, break loop
                        break

                for x, y in coords:
                    player.grid[x][y].cookie = name

    async def print_grids(self) -> None:
        # Convert squares into Emoji

        boards = [
            self.format_grid(player, emojiset)
            for emojiset in (HIDDEN_EMOJIS, COOKIE_EMOJIS)
            for player in (self.p1, self.p2)
        ]

        locations = (
            (self.p2, "opponent_board"), (self.p1, "opponent_board"),
            (self.p1, "board"), (self.p2, "board")
        )

        for board, location in zip(boards, locations):
            player, attr = location
            if getattr(player, attr):
                await getattr(player, attr).edit(content=board)
            else:
                setattr(player, attr, await player.user.send(board))

    def predicate(self, message: discord.Message) -> bool:
        if message.author == self.turn.user and message.channel == self.turn.user.dm_channel:
            if message.content.lower() == "surrender":
                self.surrender = True
                return True
            self.match = re.match("([A-E]|[a-e]) ?((5)|[1-4])", message.content.strip())
            if not self.match:
                self.bot.loop.create_task(message.add_reaction(CANCEL))
            return bool(self.match)

    async def take_turn(self) -> typing.Optional[Square]:
        square = None
        turn_message = await self.turn.user.send(
            "It's your turn! Type the square you want to aim at, first the letter then number, example: `A1`\nType **surrender** to surrender yourself."
        )
        await self.next.user.send("Their turn", delete_after=2.0)
        while True:
            try:
                await self.bot.wait_for("message", check=self.predicate, timeout=60.0)
            except asyncio.TimeoutError:
                await self.turn.user.send("You took too long. Game over!")
                await self.next.user.send(f"{self.turn.user} took too long. Game over!")
                await self.public_channel.send(
                    f"Game over! {self.turn.user.mention} timed out so {self.next.user.mention} wins and gets 100 cookies!"
                )
                AWARD_API = os.environ.get('AWARD_API')
                for i in self.bot.listcookies:
                    if i[1] == self.next.user.id:
                        winnername = i[0]
                    data = {"username":winnername, "amount": "100"}
                    credentials = json.dumps(data)
                    async with request("POST", AWARD_API, data=credentials, headers={'Content-type':'application/json', 'Accept':'application/json'}) as response:
                        pass

                self.gameover = True
                break
            else:
                if self.surrender:
                    await self.next.user.send(f"{self.turn.user} surrendered. Game over!")
                    await self.public_channel.send(
                        f"Game over! {self.turn.user.mention} surrendered to {self.next.user.mention} and earned 150 cookies!"
                    )
                    AWARD_API = os.environ.get('AWARD_API')
                    for i in self.bot.listcookies:
                        if i[1] == self.next.user.id:
                            winnername = i[0]
                        data = {"username":winnername, "amount": "150"}
                        credentials = json.dumps(data)
                        async with request("POST", AWARD_API, data=credentials, headers={'Content-type':'application/json', 'Accept':'application/json'}) as response:
                            pass

                    self.gameover = True
                    break
                square = self.get_square(self.next.grid, self.match.string)
                if square.aimed:
                    await self.turn.user.send("You've already aimed at this square.", delete_after=3.0)
                else:
                    break
        await turn_message.delete()
        return square

    async def hit(self, square: Square, alert_messages: typing.List[discord.Message]) -> None:
        await self.turn.user.send("Found!", delete_after=2.0)
        alert_messages.append(await self.next.user.send("Found!"))
        if self.check_sink(self.next.grid, square.cookie):
            await self.turn.user.send(f"You've found their {square.cookie} cookie!", delete_after=3.0)
            alert_messages.append(await self.next.user.send(f"Oh no! Your {square.cookie} was found !"))
            if self.check_gameover(self.next.grid):
                await self.turn.user.send("You win!")
                await self.next.user.send("You lose!")
                self.gameover = True
                await self.game_over(winner=self.turn.user, loser=self.next.user)

    async def start_game(self) -> None:
        await self.p1.user.send(f"You're playing Cookie Hunt with {self.p2.user}, 100 Cookies have been credited from your balance.")
        await self.p2.user.send(f"You're playing Cookie Hunt with {self.p1.user}, 100 Cookies have been credited from your balance.")

        FEE_API = os.environ.get('FEE_API')
        for i in self.bot.listcookies:
            if i[1] == self.p1.user.id:
                p1name = i[0]
        data = {"username":p1name, "amount": "100"}
        credentials = json.dumps(data)
        async with request("POST", FEE_API, data=credentials, headers={'Content-type':'application/json', 'Accept':'application/json'}) as response:
            pass

        FEE_API = os.environ.get('FEE_API')
        for i in self.bot.listcookies:
            if i[1] == self.p2.user.id:
                p2name = i[0]
        data = {"username":p2name, "amount": "100"}
        credentials = json.dumps(data)
        async with request("POST", FEE_API, data=credentials, headers={'Content-type':'application/json', 'Accept':'application/json'}) as response:
            pass

        alert_messages = []

        self.turn = self.p1
        self.next = self.p2

        while True:
            await self.print_grids()

            if self.gameover:
                return

            square = await self.take_turn()
            if not square:
                return
            square.aimed = True

            for message in alert_messages:
                await message.delete()

            alert_messages = []
            alert_messages.append(await self.next.user.send(f"{self.turn.user} aimed at {self.match.string}!"))

            if square.cookie:
                await self.hit(square, alert_messages)
                if self.gameover:
                    return
            else:
                await self.turn.user.send("Miss!", delete_after=3.0)
                alert_messages.append(await self.next.user.send("Miss!"))

            self.turn, self.next = self.next, self.turn


class CookieHunt(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.games: typing.List[Game] = []
        self.waiting: typing.List[discord.Member] = []

    def predicate(
        self,
        ctx: commands.Context,
        announcement: discord.Message,
        reaction: discord.Reaction,
        user: discord.Member
    ) -> bool:
        if self.already_playing(ctx.author):  # If they've joined a game since requesting a player 2
            return True  # Is dealt with later on
        if (
            user.id not in (ctx.me.id, ctx.author.id)
            and str(reaction.emoji) == ACCEPT
            and reaction.message.id == announcement.id
        ):
            if self.already_playing(user):
                self.bot.loop.create_task(ctx.send(f"{user.mention} You're already playing a game!"))
                self.bot.loop.create_task(announcement.remove_reaction(reaction, user))
                return False

            if user in self.waiting:
                self.bot.loop.create_task(ctx.send(
                    f"{user.mention} Please cancel your game first before joining another one."
                ))
                self.bot.loop.create_task(announcement.remove_reaction(reaction, user))
                return False

            return True

        if (
            user.id == ctx.author.id
            and str(reaction.emoji) == CANCEL
            and reaction.message.id == announcement.id
        ):
            return True
        return False

    def already_playing(self, player: discord.Member) -> bool:
        return any(player in (game.p1.user, game.p2.user) for game in self.games)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def cookiehunt(self, ctx: commands.Context) -> None:
        result = any(item[1] == ctx.author.id for item in self.bot.listcookies)
        if result == False:
            await ctx.send("You need to login to start a match.\n Use the command `?login` to login to CashOut Cookie.")
        else:
            if self.already_playing(ctx.author):
                return await ctx.send("You're already playing a game.")

            if ctx.author in self.waiting:
                return await ctx.send("You've already sent out a request for a player 2")

            announcement = await ctx.send(
                "**Cookie Hunt**: A new game is about to start!\n"
                f"Press {ACCEPT} to play against {ctx.author.name}!\n"
                f"(Cancel the game with {CANCEL})"
            )
            self.waiting.append(ctx.author)
            await announcement.add_reaction(ACCEPT)
            await announcement.add_reaction(CANCEL)

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add",
                    check=partial(self.predicate, ctx, announcement),
                    timeout=180.0
                )
            except asyncio.TimeoutError:
                self.waiting.remove(ctx.author)
                await announcement.delete()
                return await ctx.send(f"{ctx.author.mention} Seems like there's no one here to play :(")

            if str(reaction.emoji) == CANCEL:
                self.waiting.remove(ctx.author)
                await announcement.delete()
                return await ctx.send(f"Game cancelled {ctx.author.name}.")

            await announcement.delete()
            self.waiting.remove(ctx.author)
            if self.already_playing(ctx.author):
                return
            try:
                game = Game(self.bot, ctx.channel, ctx.author, user)
                result = any(item[1] == user.id for item in self.bot.listcookies)
                if result == False:
                    await ctx.send(f"You need to login to play {user.mention}.\n Use the command `?login` to login to CashOut Cookie.\n {ctx.author.mention} Game got cancelled because {user.name} tried to play without logging in, Blame him not me lel, anyways you gotta start again.")
                else:
                    self.games.append(game)
                    await game.start_game()
                    self.games.remove(game)
            except discord.Forbidden :
                await ctx.send(
                    f"{ctx.author.mention} {user.mention} "
                    "Game failed. This is likely due to you not having your DMs open. Check and try again."
                )
                self.games.remove(game)
            except Exception:
                # End the game in the event of an unforseen error so the players aren't stuck in a game
                await ctx.send(f"{ctx.author.mention} {user.mention} An error occurred. Game failed")
                self.games.remove(game)
                raise

    @cookiehunt.command(name="ships", aliases=["cookies"])
    async def battleship_ships(self, ctx: commands.Context) -> None:
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.add_field(name="Name", value="\n".join(COOKIES))
        embed.add_field(name="Size", value="\n".join(str(size) for size in COOKIES.values()))
        await ctx.send(embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(CookieHunt(bot))