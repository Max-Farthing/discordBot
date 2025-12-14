import discord

def create_game_embed_list(games):
    embeds = []
    
    #loop through all games in week
    for game in games:

        name = game["name"]
        competition = game["competitions"][0]
        state = competition["status"]["type"]["state"]
            
        #determine what color to make Embed object
        color = calculate_embed_color(state)

        #create Embed object
        embed = discord.Embed(
            title=name,
            color=color,
        )

        #Gameclock or Game details based upon state of game
        time = competition["status"]["type"]["shortDetail"]
        embed.add_field(name="", value=time, inline=False)

        #grab team information
        team1 = competition["competitors"][0]
        team2 = competition["competitors"][1]

        team1_abbr = team1["team"]["abbreviation"]
        team2_abbr = team2["team"]["abbreviation"]

        team1_logo = team1["team"]["logo"]
        team2_logo = team2["team"]["logo"]

        team1_score = int(team1["score"])
        team2_score = int(team2["score"])

        team1_record = team1["records"][0]["summary"]
        team2_record = team2["records"][0]["summary"]

        team1_score_header = f"{team1_abbr} ({team1_record})"
        team2_score_header = f"{team2_abbr} ({team2_record})"

            #set teams and scores
        if state == "post" and team1_score > team2_score:
            embed.add_field(name=f"{team1_score_header} 🏆", value=team1_score, inline=True)
            embed.add_field(name=team2_score_header, value=team2_score, inline=True)
            embed.set_thumbnail(url=team1_logo)
        elif state == "post" and team2_score > team1_score:
            embed.add_field(name=team1_score_header, value=team1_score, inline=True)
            embed.add_field(name=f"{team2_score_header} 🏆", value=team2_score, inline=True)
            embed.set_thumbnail(url=team2_logo)
        else:
            embed.add_field(name=team1_score_header, value=team1_score, inline=True)
            embed.add_field(name=team2_score_header, value=team2_score, inline=True)

        #append embed to list of embeds
        embeds.append(embed)
    return embeds

def calculate_embed_color(state):
    if state == "pre":
        return discord.Colour.from_str("#95A5A6")
    elif state == "in":
        return discord.Colour.from_str("#2ECC71")
    else:
        return discord.Colour.from_str("#C0392B")
    