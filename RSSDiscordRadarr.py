import json
from datetime import datetime
from discord.ext import commands
from tmdbv3api import TMDb, Movie
import requests
import discord
import configparser


# local log file function
def write_log(file_name, log_msg):
    # print out to console as well
    print(log_msg)

    with open(file_name, 'a') as log:
        log.write("{0},{1}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(log_msg)))


# create local log file
my_log_file = "LOG-" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
print("My log file is " + my_log_file)
write_log(my_log_file, "Discordarr started.")

# config parser - to read from config file
parser = configparser.ConfigParser()
parser.read('discordarr.config')
write_log(my_log_file, "Loaded config file discordarr.config")

# radarr connection
radarr_host_url = parser.get('radarr', 'radarrhosturl')
radarr_api_key = parser.get('radarr', 'radarrapikey')
write_log(my_log_file, "Loaded Radarr configuration.")
radarrSession = requests.Session()

# discord bot connection
bot_prefix = parser.get('bot', 'botprefix')
bot_token = parser.get('bot', 'bottoken')
bot_channel = parser.get('bot', 'botchannel')
bot = commands.Bot(command_prefix=bot_prefix)
write_log(my_log_file, "Connected to Discord bot api.")
write_log(my_log_file, "Bot Prefix: " + bot_prefix)
write_log(my_log_file, "Bot Channel: " + bot_channel)


# discord bot functions
@bot.command()
async def ping(ctx):
    await ctx.send('yes - Discordarr is alive!')


@bot.command()
async def checknew(ctx):
    # the moviedatabase connection
    # needs to be at each function call to do a "refresh"
    tmdbapi = TMDb()
    tmdbapi.api_key = parser.get('tmdb', 'tmdbapikey')
    tmdbapi.language = parser.get('tmdb', 'tmdblanguage')
    tmdbapi.debug = True
    write_log(my_log_file, "Loaded TMDB configuration.")

    # pulling all the movies in the radarr db
    radarrMovies = radarrSession.get('{0}/api/movie?apikey={1}'.format(radarr_host_url, radarr_api_key))
    write_log(my_log_file, "Connected to Radarr movie api.")
    # list that contains all the moviedb ids that exist in radarr db
    ids = []
    # go through the json and pull all tmdb ids into an array
    for title in radarrMovies.json():
        ids.append(title["tmdbId"])
    write_log(my_log_file, "Loaded all the current TMDB movies ids into memory that exist in your Radarr library.")

    # get upcoming movies to blu ray from themoviedb
    movies = Movie()
    upcomingmovies = movies.upcoming()

    # go through all the movies that came out this month and if they dont exist in radarr post them to discord
    for movie in upcomingmovies:
        # if the movie doesnt exist in radarr post to discord
        if movie.id not in ids:
            embed = discord.Embed(title=movie.title + " [" + str(movie.id) + "]", colour=discord.Colour(0xb45818),
                                  url="http://image.tmdb.org/t/p/w185" + str(movie.poster_path),
                                  description=movie.overview)
            embed.set_thumbnail(url="http://image.tmdb.org/t/p/w185" + str(movie.poster_path))
            embed.set_author(name="Discordarr")
            embed.set_footer(text=movie.id)
            emoji = '\N{THUMBS UP SIGN}'
            m = await ctx.send(content=movie.title + " (Released: " + movie.release_date + ")", embed=embed)
            await m.add_reaction(emoji)

            write_log(my_log_file, "Title: " + movie.title + " [" + str(
                movie.id) + "]" + "Release Date: " + movie.release_date + "Overview: "
                      + movie.overview + "Poster Path: " + str(movie.poster_path))


@bot.command()
async def checkpop(ctx):
    # the moviedatabase connection
    # needs to be at each function call to do a "refresh"
    tmdbapi = TMDb()
    tmdbapi.api_key = parser.get('tmdb', 'tmdbapikey')
    tmdbapi.language = parser.get('tmdb', 'tmdblanguage')
    tmdbapi.debug = True
    write_log(my_log_file, "Loaded TMDB configuration.")

    # pulling all the movies in the radarr db
    radarrMovies = radarrSession.get('{0}/api/movie?apikey={1}'.format(radarr_host_url, radarr_api_key))
    write_log(my_log_file, "Connected to Radarr movie api.")
    # list that contains all the moviedb ids that exist in radarr db
    ids = []
    # go through the json and pull all tmdb ids into an array
    for title in radarrMovies.json():
        ids.append(title["tmdbId"])
    write_log(my_log_file, "Loaded all the current TMDB movies ids into memory that exist in your Radarr library.")

    # get upcoming movies to blu ray from themoviedb
    movies = Movie()
    popularmovies = movies.popular()

    # go through all the movies that came out this month and if they dont exist in radarr post them to discord
    for movie in popularmovies:
        # if the movie doesnt exist in radarr post to discord
        if movie.id not in ids:
            embed = discord.Embed(title=movie.title + " [" + str(movie.id) + "]", colour=discord.Colour(0xb45818),
                                  url="http://image.tmdb.org/t/p/w185" + str(movie.poster_path),
                                  description=movie.overview)
            embed.set_thumbnail(url="http://image.tmdb.org/t/p/w185" + str(movie.poster_path))
            embed.set_author(name="Discordarr")
            embed.set_footer(text=movie.id)
            emoji = '\N{THUMBS UP SIGN}'
            m = await ctx.send(content=movie.title + " (Released: " + movie.release_date + ")", embed=embed)
            await m.add_reaction(emoji)

            write_log(my_log_file, "Title: " + movie.title + " [" + str(
                movie.id) + "]" + "Release Date: " + movie.release_date + "Overview: "
                      + movie.overview + "Poster Path: " + str(movie.poster_path))


@bot.command()
async def checknowplaying(ctx):
    # the moviedatabase connection
    # needs to be at each function call to do a "refresh"
    tmdbapi = TMDb()
    tmdbapi.api_key = parser.get('tmdb', 'tmdbapikey')
    tmdbapi.language = parser.get('tmdb', 'tmdblanguage')
    tmdbapi.debug = True
    write_log(my_log_file, "Loaded TMDB configuration.")

    # pulling all the movies in the radarr db
    radarrMovies = radarrSession.get('{0}/api/movie?apikey={1}'.format(radarr_host_url, radarr_api_key))
    write_log(my_log_file, "Connected to Radarr movie api.")
    # list that contains all the moviedb ids that exist in radarr db
    ids = []
    # go through the json and pull all tmdb ids into an array
    for title in radarrMovies.json():
        ids.append(title["tmdbId"])
    write_log(my_log_file, "Loaded all the current TMDB movies ids into memory that exist in your Radarr library.")

    # get upcoming movies to blu ray from themoviedb
    movies = Movie()
    nowplayingmovies = movies.now_playing()

    # go through all the movies that came out this month and if they dont exist in radarr post them to discord
    for movie in nowplayingmovies:
        # if the movie doesnt exist in radarr post to discord
        if movie.id not in ids:
            embed = discord.Embed(title=movie.title + " [" + str(movie.id) + "]", colour=discord.Colour(0xb45818),
                                  url="http://image.tmdb.org/t/p/w185" + str(movie.poster_path),
                                  description=movie.overview)
            embed.set_thumbnail(url="http://image.tmdb.org/t/p/w185" + str(movie.poster_path))
            embed.set_author(name="Discordarr")
            embed.set_footer(text=movie.id)
            emoji = '\N{THUMBS UP SIGN}'
            m = await ctx.send(content=movie.title + " (Released: " + movie.release_date + ")", embed=embed)
            await m.add_reaction(emoji)

            write_log(my_log_file, "Title: " + movie.title + " [" + str(
                movie.id) + "]" + "Release Date: " + movie.release_date + "Overview: "
                      + movie.overview + "Poster Path: " + str(movie.poster_path))


@bot.command()
async def checktoprated(ctx):
    # the moviedatabase connection
    # needs to be at each function call to do a "refresh"
    tmdbapi = TMDb()
    tmdbapi.api_key = parser.get('tmdb', 'tmdbapikey')
    tmdbapi.language = parser.get('tmdb', 'tmdblanguage')
    tmdbapi.debug = True
    write_log(my_log_file, "Loaded TMDB configuration.")

    # pulling all the movies in the radarr db
    radarrMovies = radarrSession.get('{0}/api/movie?apikey={1}'.format(radarr_host_url, radarr_api_key))
    write_log(my_log_file, "Connected to Radarr movie api.")
    # list that contains all the moviedb ids that exist in radarr db
    ids = []
    # go through the json and pull all tmdb ids into an array
    for title in radarrMovies.json():
        ids.append(title["tmdbId"])
    write_log(my_log_file, "Loaded all the current TMDB movies ids into memory that exist in your Radarr library.")

    # get upcoming movies to blu ray from themoviedb
    movies = Movie()
    topratedmovies = movies.top_rated()

    # go through all the movies that came out this month and if they dont exist in radarr post them to discord
    for movie in topratedmovies:
        # if the movie doesnt exist in radarr post to discord
        if movie.id not in ids:
            embed = discord.Embed(title=movie.title + " [" + str(movie.id) + "]", colour=discord.Colour(0xb45818),
                                  url="http://image.tmdb.org/t/p/w185" + str(movie.poster_path),
                                  description=movie.overview)
            embed.set_thumbnail(url="http://image.tmdb.org/t/p/w185" + str(movie.poster_path))
            embed.set_author(name="Discordarr")
            embed.set_footer(text=movie.id)
            emoji = '\N{THUMBS UP SIGN}'
            m = await ctx.send(content=movie.title + " (Released: " + movie.release_date + ")", embed=embed)
            await m.add_reaction(emoji)

            write_log(my_log_file, "Title: " + movie.title + " [" + str(
                movie.id) + "]" + "Release Date: " + movie.release_date + "Overview: "
                      + movie.overview + "Poster Path: " + str(movie.poster_path))


@bot.command()
async def getmovie(ctx, arg):
    write_log(my_log_file, "GetMovie command requested tmdbid " + arg)

    # add tmdb movie id to radarr via apii
    movie = Movie()
    moviedetails = movie.details(arg)

    # prepare dictionary json
    movieaddjson = {"title": moviedetails.title,
                    "qualityProfileId": 1,
                    "titleSlug": moviedetails.title.lower().replace(' ', '-') + "-" + str(moviedetails.id),
                    "images": [
                        {"covertype": "poster", "url": "https://image.tmdb.org/t/p/w200" + moviedetails.poster_path}],
                    "tmdbId": moviedetails.id,
                    "profileId": 1,
                    "year": int(datetime.strptime(moviedetails.release_date, '%Y-%m-%d').year),
                    "rootFolderPath": "/movies/",
                    "monitored": True,
                    "addOptions": {"searchForMovie": True}
                    }
    write_log(my_log_file, "Add Movie Request: " + json.dumps(movieaddjson))

    # post the add movie request
    radarraddmovie = radarrSession.post('{0}/api/movie?apikey={1}'.format(radarr_host_url, radarr_api_key),
                                        json=movieaddjson)

    write_log(my_log_file, str(radarraddmovie.json()))

    # post to discord - completed message
    embed = discord.Embed(title=moviedetails.title + " [" + str(moviedetails.id) + "]", colour=discord.Colour(0x96ff00),
                          url="http://image.tmdb.org/t/p/w185" + str(moviedetails.poster_path),
                          description=moviedetails.overview)
    embed.set_thumbnail(url="http://image.tmdb.org/t/p/w185" + str(moviedetails.poster_path))
    embed.set_author(name="Discordarr")
    embed.set_footer(text=moviedetails.id)
    await ctx.send(content=moviedetails.title + " (Added to Radarr)", embed=embed)

    write_log(my_log_file, moviedetails.title + " has been added to Radarr, set to monitored and search has started!")


@bot.event
async def on_reaction_add(reaction, user):
    if user.id != bot.user.id:
        write_log(my_log_file, "Reaction requested tmdbid " + str(reaction.message.embeds[0].footer.text))

        # add tmdb movie id to radarr via apii
        movie = Movie()
        moviedetails = movie.details(int(reaction.message.embeds[0].footer.text))

        # prepare dictionary json
        movieaddjson = {"title": moviedetails.title,
                        "qualityProfileId": 1,
                        "titleSlug": moviedetails.title.lower().replace(' ', '-') + "-" + str(moviedetails.id),
                        "images": [
                            {"covertype": "poster",
                             "url": "https://image.tmdb.org/t/p/w200" + moviedetails.poster_path}],
                        "tmdbId": moviedetails.id,
                        "profileId": 1,
                        "year": int(datetime.strptime(moviedetails.release_date, '%Y-%m-%d').year),
                        "rootFolderPath": "/movies/",
                        "monitored": True,
                        "addOptions": {"searchForMovie": True}
                        }
        write_log(my_log_file, "Add Movie Request: " + json.dumps(movieaddjson))

        # post the add movie request
        radarraddmovie = radarrSession.post('{0}/api/movie?apikey={1}'.format(radarr_host_url, radarr_api_key),
                                            json=movieaddjson)

        write_log(my_log_file, str(radarraddmovie.json()))

        # post to discord - completed message
        await bot.get_channel(reaction.message.channel.id).send(
            moviedetails.title + " has been added to Radarr, set to "
                                 "monitored and search has started!")

        write_log(my_log_file,
                  moviedetails.title + " has been added to Radarr, set to monitored and search has started!")


@bot.event
async def on_message(message):
    if message.channel.name == bot_channel:
        await bot.process_commands(message)


@bot.event
async def on_ready():
    print('#############')
    print('Logged in as ' + bot.user.name)
    print('Bot user id ' + str(bot.user.id))
    print("Listening on channel " + bot_channel + " only!")
    print('#############')
    write_log(my_log_file, bot.user.name + " logged in.")


# start the bot
bot.run(bot_token)
