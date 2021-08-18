from flask import Flask, render_template, request, redirect, url_for
import requests, json, sys
import api_twitch
import io 
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

@app.route('/')
def home():
  fig,ax = plt.subplots(figsize=(10,8))
  ax = sns.set_style(style="dark")
  live = {}
  live['data'] = []
  live_stream = []
  response = api_twitch.get_toplive()
  data = api_twitch.print_response(response)
  #print(data)
  w = json.loads(data)
  for x in range(4):
    z = w["data"][x]
    live['data'].append(z)
  for y in range(4):
    live_stream.append(live['data'][y]['user_name'])
    live_stream.append(live['data'][y]['game_name'])
    live_stream.append(live['data'][y]['viewer_count'])
    uwu = live['data'][y]['thumbnail_url']
    thumbnail = uwu.replace('{width}x{height}', '1280x720')
    live_stream.append(thumbnail)
  data = {
    'user' : live_stream[0],
    'game' : live_stream[1],
    'visitas' : live_stream[2],
    'url' : live_stream[3],
    'user2' : live_stream[4],
    'game2' : live_stream[5],
    'visitas2' : live_stream[6],
    'url2' : live_stream[7],
    'user3' : live_stream[8],
    'game3' : live_stream[9],
    'visitas3' : live_stream[10],
    'url3' : live_stream[11],
    'user4' : live_stream[12],
    'game4' : live_stream[13],
    'visitas4' : live_stream[14],
    'url4' : live_stream[15]
  }
  x = [live_stream[0],live_stream[4],live_stream[8],live_stream[12]]
  y = [live_stream[2],live_stream[6],live_stream[10],live_stream[14]]
  sns.barplot(x,y)
  canvas=FigureCanvas(fig)
  img=io.BytesIO()
  fig.savefig('static/img/grafico.png')
  return render_template("home.html",data=data)

@app.route('/Streamer', methods=["POST","GET"])
def profile():
  query = api_twitch.get_topgames()
  data = api_twitch.print_response(query)
  #print(data)
  topGame = {}
  topGame['data'] = []
  Games = []
  w = json.loads(data)
  for x in range(6):
    z = w["data"][x]
    topGame['data'].append(z)
  for y in range(6):
    Games.append(topGame['data'][y]['id'])
    Games.append(topGame['data'][y]['name'])
    uwu = topGame['data'][y]['box_art_url']
    thumbnail = uwu.replace('{width}x{height}', '1280x720')
    Games.append(thumbnail)
  data = {
    'id' : Games[0],
    'name' : Games[1],
    'banner' : Games[2],
    'id2' : Games[3],
    'name2' : Games[4],
    'banner2' : Games[5],
    'id3' : Games[6],
    'name3' : Games[7],
    'banner3' : Games[8],
    'id4' : Games[9],
    'name4' : Games[10],
    'banner4' : Games[11],
    'id5' : Games[12],
    'name5' : Games[13],
    'banner5' : Games[14],
    'id6' : Games[15],
    'name6' : Games[16],
    'banner6' : Games[17],
  }
  if request.method == 'POST':
    user = request.form["nm"]    
    return redirect(url_for("user", usr=user))
  else:
    return render_template("detail.html", data=data)

@app.route('/Streamer/<usr>')
def user(usr):
  streamer = {}
  streamer['data'] = []
  query = api_twitch.get_user_query(usr)
  response = api_twitch.get_response(query)
  data = api_twitch.print_response(response)
  #######################
  x = json.loads(data)
  y = x["data"][0]
  streamer['data'].append(y)
  id_capo = y['id']
  queryB = api_twitch.get_follows(id_capo)
  dataB = api_twitch.print_response(queryB)
  v = json.loads(dataB)
  follows = v['total']
  #print(follows)
  #######################
  queryC = api_twitch.get_followed(id_capo)
  dataC = api_twitch.print_response(queryC)
  #print(dataC)
  h = json.loads(dataC)
  followed = h['total']
  #print(followed)
  #print(data)
  if(y['offline_image_url'] != ""):
    print('no es nulo')
    background_def = y['offline_image_url']
  else:
    print('es nulo')
    background_def = '/static/img/def.png'

  data = {
    'nombre' : usr,
    'fecha' : y['created_at'],
    'visitas' : y['view_count'],
    'partner' : y['broadcaster_type'],
    'foto_perfil' : y['profile_image_url'],
    'sumary' : y['description'],
    'offline' : background_def,
    'seguidores' : follows,
    'siguiendo' : followed
  }

  fig,ax = plt.subplots(figsize=(10,8))
  ax = sns.set_style(style="dark")
  x = ['seguidores','siguiendo']
  y = [follows,followed]
  sns.barplot(x,y)
  canvas=FigureCanvas(fig)
  img=io.BytesIO()
  fig.savefig('static/img/stats.png')

  return render_template("detail_B.html", data=data)

@app.route('/About')
def explorer():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)
