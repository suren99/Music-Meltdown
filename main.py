import urllib2
import requests
import Queue
from fuzzywuzzy import process
import time
import os
import threading
import datetime
from bs4 import BeautifulSoup
music_dir = "/Users/suren/Songs/"
no_of_threads = 100
Q = Queue.Queue()

class website:
    def __init__(self):
        self.hdr= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

    def download(self,url,mp3name,movie):
        print "Downloading " + mp3name
        req = urllib2.Request(url,headers=self.hdr)
        response = urllib2.urlopen(req)
        data = response.read()
        song = open(music_dir+movie+"/"+mp3name,"wb")
        song.write(data)
        song.close()

    def get_song_list(self,url):
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text,"html.parser")
            div_tags = soup.find_all("div",class_="mp3song");
            songs = [each_div_tags.attrs["title"] for each_div_tags in div_tags]
            links = []
            form_tags = soup.find_all("form")
            i = 0
            mod_songs = []
            for each_form_tags in form_tags:
                if len(list(each_form_tags.find_all("input",value="Download 320kbps"))) == 0 and len(list(each_form_tags.find_all("input",type="hidden"))) != 0:
                    links += ["http://www.tnhits.info/Download.php?file="+each_form_tags.find_all("input",type="hidden")[0].attrs["value"]]
                    mod_songs.append(songs[i])
                    i += 1
            return mod_songs,links
        except:
            # too many requests to the server
            time.sleep(0.2)
            return self.get_song_list(url)

    def get_movies_list(self,url):
        try:
            movies = []
            links = []
            r = requests.get(url)
            soup = BeautifulSoup(r.text,"html.parser")
            div_tags = soup.find_all("div",class_="file")
            if len(list(div_tags)) == 0:
                return None,None
            for each_div_tags in div_tags:
                links += [each_div_tags.find('a').attrs['href']]
            movies += [each_div_tag.attrs["title"] for each_div_tag in div_tags]
            return movies,links
        except:
        # too many requests to the server
            time.sleep(0.2)
            return self.get_movies_list(url)


def get_movie_name():
    print "Movie-name:"
    movie_name = raw_input()
    fp = open("movies.txt","r")
    movies_and_links = fp.readlines()
    fp.close()
    years = []
    movies = []
    links = []
    for each in movies_and_links:
        split = each.split(',')
        years.append(split[0])
        movies.append(split[1])
        links.append(split[2])
    result = process.extract(movie_name,movies,limit = 7)
    print "Do u mean?"
    index = [None] * len(result)
    d = {}
    for cnt,each_match in enumerate(result):
        all_indices_of_each_match = [i for i,x in enumerate(movies) if x == each_match[0]]
        if each_match[0] not in d:
            d[each_match[0]] = 0
        index[cnt] = all_indices_of_each_match[d[each_match[0]]]
        d[each_match[0]] += 1
        print str(cnt+1)+"."+each_match[0]+" - released in "+years[index[cnt]]
    chosen = int(raw_input())
    index = index[chosen-1]
    url = "http://www.tamilfreemp3songs.co"+links[index].replace(' ','+')
    print "\nYou have selected the movie :" + links[index].split('/')[2].replace("+"," ");
    songs,links = site.get_song_list(url);
    movie = movies[index]
    if not os.path.exists(music_dir + movie):
        os.mkdir(music_dir + movie)
    print "List of songs :"
    for cnt,each_song in enumerate(songs):
        print str(cnt+1)+"."+each_song
    print "\nPlease select the indices of the song you would like to download separated by commas"
    print "Press "+ str(len(songs) + 1) +" to download all"
    choices = raw_input().split(',')
    if str(len(songs) + 1) in choices:
        for i in range(0,len(links)):
            site.download(links[i], songs[i], movies[index])
    else:
        for each in choices:
            site.download(links[int(each)-1], songs[int(each)-1], movies[index])
    print "Download complete"
    fp = open("last_downloaded.txt","w")
    fp.write(music_dir + "" + movie)
    fp.close()

def get_song_name():
    print "Song name:"
    song_name = raw_input()
    fp = open("songs.txt")
    songs_and_links = fp.readlines()
    fp.close()
    songs = []
    links = []
    movies = []
    for each in songs_and_links:
        each_song_link_movie = each.split(',')
        songs.append(each_song_link_movie[1])
        links.append(each_song_link_movie[2])
        movies.append(each_song_link_movie[3].replace("\n",""))
    result = process.extract(song_name, songs, limit = 10)
    print "Do u mean?"
    index = [None] * len(result)
    d = {}
    for cnt,each_match in enumerate(result):
        all_indices_of_each_match = [i for i,x in enumerate(songs) if x == each_match[0]]
        if each_match[0] not in d:
            d[each_match[0]] = 0
        index[cnt] = all_indices_of_each_match[d[each_match[0]]]
        d[each_match[0]] += 1
        print str(cnt+1)+"."+each_match[0]+" from "+movies[index[cnt]]
    chosen = int(raw_input())
    index = index[chosen-1]
    site.download(links[index],songs[index],"")
    print "Download complete"
    fp = open("last_downloaded.txt","w")
    fp.write(music_dir+""+songs[index])
    fp.close()

ml_lock = threading.Lock()
sl_lock = threading.Lock()
movies_list = set()
songs_list = set()

def work():
    global movies_list, songs_list
    while True:
        url,work_type,year = Q.get()
        if url is None:
            break
        if work_type == "movie":
            movies,links = site.get_movies_list(url)
            if movies is not None:
                ml_lock.acquire()
                movies_list.update([year+","+each_movie+","+each_link for each_movie,each_link in zip(movies,links)])
                for each_movie in movies:
                    Q.put(("http://tamilfreemp3songs.co/Movie/"+each_movie,"songs",year))
                ml_lock.release()
        else:
            songs,links = site.get_song_list(url)
            sl_lock.acquire()
            songs_list.update([year+","+each_song+","+each_link+","+url.replace("http://tamilfreemp3songs.co/Movie/","") for each_song,each_link in zip(songs,links)])
            sl_lock.release()
        Q.task_done()

def go():
    print "Please wait for some time....."
    thread = [None] * no_of_threads
    for i in range(no_of_threads):
        thread[i] = threading.Thread(target = work)
        thread[i].start()
    fp = open("updated_year.txt","r")
    current_year = datetime.datetime.now().year
    fp_read = fp.readline()
    fp.close()
    if fp_read != '':
        last_updated_year = int(fp_read)
    else:
        last_updated_year = 1977
    total_range = list(map(str,range(last_updated_year, current_year + 1)))
    # Queue up the work
    for each_range in total_range:
        for each_page in range(20):
            Q.put(("http://www.tamilfreemp3songs.co/Year/"+each_range+"?page="+str(each_page + 1),"movie",each_range))
    Q.join()
    # Calm up the workers
    for i in range(no_of_threads):
        Q.put((None,None,None))
    for i in range(no_of_threads):
        thread[i].join()
        fp = open("movies.txt","r")
    movies_file_list = fp.readlines()
    fp.close()
    fp = open("movies.txt","w")
    final = set()
    for i in movies_file_list:
        split = i.split(",")
        if int(split[0]) != last_updated_year:
            final.add(i.replace("\n",""))
    final.update(movies_list)
    fp.write('\n'.join(final))
    fp.close()
    fp = open("songs.txt","r")
    songs_file_list = fp.readlines()
    fp.close()
    fp = open("songs.txt", "w")
    final = set()
    for i in songs_file_list:
        split = i.split(",")
        if int(split[0]) != last_updated_year:
             final.add(i.replace("\n",""))
    final.update(songs_list)
    fp.write('\n'.join(final))
    fp.close()
    fp = open("updated_year.txt","w")
    fp.write(str(current_year))
    fp.close()
    print "Refresh completed"

if __name__ == "__main__":
    start = time.time()
    site = website()
    options = {1:get_movie_name,2:get_song_name,3:go,4:go}
    print "1.Download by movie name\n2.Download by song name\n3.Refresh\n4.Full refresh"
    chosen = int(raw_input())
    if chosen == 4:
        fp = open("updated_year.txt","w")
        fp.write("1977");
        fp.close()
        open("movies.txt", "w").close()
        open("songs.txt", "w").close()
    options[chosen]()
    print "time taken : "+str(time.time() - start)+" secs"
