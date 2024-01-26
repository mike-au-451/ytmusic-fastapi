import pathlib

from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

# import starlette.status as status
from starlette import status

from ytmusicapi import YTMusic

app = FastAPI()

ytm = ""
playlists = []
currentpl = ""
currentid = ""
tracklist = []

templates = Jinja2Templates(directory = [ pathlib.Path(__file__).parent / "templates" ])

app.mount("/static", StaticFiles(directory = "static"), name = "static")

@app.get("/", response_class = HTMLResponse)
def hRoot(req: Request):
	context = {
		"request": req,
		"title": currentpl,
		"playlists": playlists,
		"tracks": tracklist
	}
	return templates.TemplateResponse("index.html", context)

@app.post("/refresh", response_class = HTMLResponse)
async def hRefresh(req: Request):
	global playlists, currentpl, currentid, tracklist

	body = await req.body()

	elems = body.split(b'=')
	if len(elems) != 2:
		return HTTPException(status_code = 400, detail = "missing playlist")

	postid = elems[1].decode()

	refresh()
	currentpl = ""
	currentid = ""
	for pl in playlists:
		if pl["id"] == postid:
			currentpl = pl["name"]
			currentid = pl["id"]
			break

	if currentid != "":
		pl = ytm.get_playlist(currentid, limit = None)
		tracklist = []
		for tr in pl["tracks"]:
			title = "missing"
			artists = "missing"
			album = "missing"
			if "title" in tr:
				title = tr["title"]
			if "artists" in tr:
				al = []
				for ar in tr["artists"]:
					if "name" in ar:
						al.append(ar["name"])
				artists = ", ".join(al)

			if "album" in tr and tr["album"] is not None:
				if "name" in tr["album"]:
					album = tr["album"]["name"]

			tracklist.append({ "title": title, "artists": artists, "album": album})
			

	return RedirectResponse(url = "/", status_code = status.HTTP_302_FOUND)

def refresh():
	global playlists, currentpl

	pls = ytm.get_library_playlists()
	playlists = []
	for pl in pls:
		playlists.append({ "id": pl["playlistId"], "name": pl["title"]})
	if currentpl == "":
		currentpl = "Pick something!"
		currentid = ""

ytm = YTMusic("oauth.json")
refresh()

