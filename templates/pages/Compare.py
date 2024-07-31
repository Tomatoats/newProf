import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pages import models
from yattag import Doc, indent
#getplaylists,clean,gettoken,compare,callSpotify Work
#now that we have id's, we can start making  the website


def ult(dif1,same,dif2):
     #Now we put in one big list.
    ultlist = []
    for x in range(len(dif1)):
        li = dif1[x]
        s = same[x]
        t = dif2[x]
        list1 = li + s + t
        ultlist.append(list1)
    return ultlist

def buildCompare(d1list,slist,d2list):
    #I think here we're just gonna clean up the lists to have it be clean
    biglength = len(d1list) if len(d1list) >= len(d2list) else len(d2list)
    #Making the dicts the same length with emptiness
    leftover = biglength - len(d1list)
    for x in range(leftover):
        toAdd = ["","","","",""]
        d1list.append(toAdd)

    leftover = biglength - len(slist)
    for x in range(leftover):
        toAdd = ["","","","",""]
        slist.append(toAdd)
    leftover = biglength - len(d2list)
    for x in range(leftover):
        toAdd = ["","","","",""]
        d2list.append(toAdd)

    return d1list,slist,d2list


    #<table>
        #<tr>
            #<th>Same</th>
            #<th>Unique in Playlist 1</th>
            #<th>Unique in Playlist 2</th>
        #</tr>
    # So we need a tr as long as the longest playlist
    # and three td's, one for same, one for dif1, one for dif2
    # once it's done on one side we leave that td blank
    # inside the td will be name,artist, an album image, and when you hover and click on the image you can play the song
    #  





def addtoModels(dif1,same,dif2,songs):
    d1 = []
    sm = []
    d2 = []  
    slist = []
    d1list = []
    d2list = []
    #We set up empty lists, the major lists will be 2d lists, so [][], and the smaller ones will be our parts in that

    #We do the same thing for each list: get pid, all the info we need, put em into one list, put that list into another one.
    for x in same:
        sm = [x]
        el = songs.get(x)
        sm = sm + el

        slist.append(sm)

    for x in dif1:
        d1 = [x]
        el = songs.get(x)
        d1 = d1 + el
        d1list.append(d1)

    for x in dif2:
        d2 = [x]
        el = songs.get(x)
        d2 = d2 + el
        d2list.append(d2)

    #We take these to buildCompare to fluff up them lists with appropiate empty space
    d1list,slist,d2list = buildCompare(d1list,slist,d2list)
    return d1list,slist,d2list
   



def clean(playlist):
     play = playlist[34:] #chopping off the htps:// open.spotify shenanigans
     p =  play[:22] # sometimes there's more than meets the eye
     return p


def getToken():
    #this is just client id's and secrets for the spotifyapi
    clid = "432742e8cdd04d149d847dd79a797024"
    clet = "69a867f4a0544550bf6c10e2f94b26c2"
    yuri = "http://alexys.online/projects/Compare"
    scope = ""
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clid,client_secret=clet))
    return sp

    


def compare(id1,id2):
    set1 = set(id1)
    set2 = set(id2)
    #Turn them into sets and get intersections and differences of them
    #That way we can get unique and not unique songs 
    intersection = set1.intersection(set2)
    difset1 = set1.difference(intersection)
    difset2 = set2.difference(intersection)

    dif1 = list(difset1)
    dif2 = list(difset2)
    same = list(intersection)
    #return them back into a list

    #addtoModels(dif1,same,dif2)
    return dif1,same,dif2




def callSpotify(p,thisdict):
    offset = 0
    sp = getToken()
   #We need a token in order to call spotify's api

    flag = True
    songids = []
  #Setting up for loops and holding info
    count = 0
    while flag == True:
        results = sp.playlist_items(p,offset=offset,fields='items.track',additional_types=['track'])
        
        if len(results['items']) == 0:
            flag = False
        
        offset = offset + len(results['items'])
        #The previous steps just make sure we keep iterating since the spotify api only allows us to get
        #up to a hundred songs per capture

        for idx, track in enumerate(results['items']):
            #This for loops add the info from the results into a list and a song dict. We'll use the info to pool info again later
            listing = []
            
            songids.append(str(track['track']['id']))
            pid = str(track['track']['id']) #pid
            listing.append(str(track['track']['name'])) #name
            listing.append(str(track['track']['artists'][0]['name'])) #artist
            listing.append(str(track['track']['preview_url'])) #audio
            listing.append(str(track['track']['album']['images'][2]['url'])) #album
            # pid = 0, name = 1, artist = 2, audio = 3, album = 4

            
            thisdict.update({pid:listing})
           
        count +=1
    results = sp.user_playlist(user=None, playlist_id=p,fields="name")
    name = results["name"]
    return songids,thisdict,name


    

def getPlaylists(play1,play2):
    p1 = clean(play1)
    p2 = clean(play2)
    #cleans the link to give us the info we actually need: the playlist id
    songdict= {}
    id1,songdict,p1Name =  callSpotify(p1,songdict)
    id2,songdict,p2Name = callSpotify(p2,songdict)
    #we do this twice  to keep the song dict reiterating
    

    dif1, same, dif2 = compare(id1,id2)
    #This gives us our different lists and our same list of id for songs
    length = [len(same),len(dif1),len(dif2),p1Name,p2Name]
    biglength = length[1] if length[1] >= length[2] else length[2]
    #this is for later reiterating purposes and getting that info for the table

    dif1,same,dif2 =addtoModels(dif1,same,dif2,songdict)
    #from here we fluff up the lists for the table with empty strings and get em to the right size for the table
    # this also connects our song id's to the info we need via the songdict


    
    ultlist = ult(dif1,same,dif2)
    # I didn't wanna do this but i couldn't find a way to iterate over 3 seperate lists so i  put em all together to iterate on in the table
    return ultlist,length,biglength
    #todo: Have a dict for all the song stuff we need, sets to show, and then we go down and find all the dict for said lists so that we don't have to results twice
    
