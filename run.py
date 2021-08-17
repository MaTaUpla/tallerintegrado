from flask import Flask, render_template, request, redirect, url_for
import requests, json, sys
import api_twitch

app = Flask(__name__)

@app.route('/')
def home():
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
  return render_template("home.html",data=data)

@app.route('/Streamer', methods=["POST","GET"])
def profile():
  if request.method == 'POST':
    user = request.form["nm"]    
    return redirect(url_for("user", usr=user))
  else:
    return render_template("detail.html")

@app.route('/Streamer/<usr>')
def user(usr):
  streamer = {}
  streamer['data'] = []
  query = api_twitch.get_user_query(usr)
  response = api_twitch.get_response(query)
  data = api_twitch.print_response(response)
  x = json.loads(data)
  y = x["data"][0]
  streamer['data'].append(y)
  print(data)
  data = {
    'nombre' : usr,
    'fecha' : y['created_at'],
    'visitas' : y['view_count'],
    'partner' : y['broadcaster_type'],
    'foto_perfil' : y['profile_image_url']
  }
  return render_template("detail_B.html", data=data)

@app.route('/About')
def explorer():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)
