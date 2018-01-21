import urllib2
import requests
from fuzzywuzzy import process
import os
from bs4 import BeautifulSoup
music_dir ="/Users/suren/Songs/"
class website:
        def __init__(self):
                self.hdr= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                                     'Accept-Encoding': 'none',
                                            'Accept-Language': 'en-US,en;q=0.8',
                                                   'Connection': 'keep-alive'}

        def download(self,i,url,mp3name,movie):
                req=urllib2.Request(url,headers=self.hdr)
                response=urllib2.urlopen(req)
                data=response.read()
                song=open(music_dir+movie+"/"+mp3name,"wb")
                song.write(data)
                song.close()


        def get_song_list(self,url):
                r=requests.get(url)
                soup=BeautifulSoup(r.text,"html.parser")
                div_tags=soup.find_all("div",class_="mp3song");
                songs=[each_div_tags.attrs["title"] for each_div_tags in div_tags]
                return songs

        def download_songs(self,movie,url):
                url="http://tamilfreemp3songs.com/"+url
                print "Downloading songs from "+ movie+"...\n"
                songs= self.get_song_list(url)
                print "List Of Songs: \n"
                for each in songs:
                        converted_string= each.encode('ascii')
                        if ".zip" in converted_string:
                                break
                        print converted_string.replace('.mp3','')
                print ''
                r=requests.get(url)
                soup=BeautifulSoup(r.text,"html.parser")
                form_tags=soup.find_all("form")
                i=0
                movie=movie.replace('\n','')
                if not os.path.exists("/Users/suren/Songs/"+movie):
                        os.mkdir("/Users/suren/Songs/"+movie)
                for each_form_tags in form_tags:
                       if len(list(each_form_tags.find_all("input",value="Download 320kbps")))==0 and len(list(each_form_tags.find_all("input",type="hidden")))!=0:
                               print "Downloading "+songs[i]
                               self.download(i,"http://www.tnhits.info/Download.php?file="+each_form_tags.find_all("input",type="hidden")[0].attrs["value"],songs[i],movie)
                               i+=1

        def get_movie_list_and_links(self):
                movies=[]
                links=[]
                for each_alphabet in list(map(chr,range(65,90))):
                        url="http://tamilfreemp3songs.com/Movies/"+each_alphabet
                        page_no=1
                        while True:
                                r=requests.get(url+'&page='+str(page_no))
                                soup=BeautifulSoup(r.text,"html.parser")
                                div_tags=soup.find_all("div",class_="file")
                                if len(list(div_tags))==0:
                                        break
                                for each_div_tags in div_tags:
                                        links+=[each_div_tags.find('a').attrs['href']]
                                movies+=[each_div_tag.attrs["title"] for each_div_tag in div_tags]
                                page_no+=1
                return movies,links

def get_movie_name():
        print "Movie-name:"
        movie_name=raw_input()
        fp = open("movie.txt","r")
        movies_and_links=fp.readlines()
        fp.close()
        movies=[]
        links=[]
        for each in movies_and_links:
               each_movie=each[:each.find(',')]
               each_link=each[each.find(',')+1:]
               movies.append(each_movie)
               links.append(each_link)
        best=get_score(movie_name,movies)
        index=movies.index(best)
        site.download_songs(best,links[index].replace(' ','+'))
        print "Download complete"

def get_score(movie_name,movies):
        result=process.extract(movie_name,movies)
        print "Do u mean?"
        for cnt,each_match in enumerate(result):
                print str(cnt+1)+"."+each_match[0]
        chosen=int(raw_input())
        return result[chosen-1][0]

def refresh():
        print "Updating the repository.Please Wait"
        movies,links=site.get_movie_list_and_links()
        fp=open("movie.txt","r")
        prev_movie_list = fp.readlines();
        fp.close()
        fp = open("movie.txt","w")
        movies=[i.encode('ascii')for i in movies]
        links=[i.encode('ascii') for i in links]
        movies_links=[each_movie+','+each_link for each_movie,each_link in zip(movies,links)]
        result='\n'.join(movies_links)
        fp.write(result)
        fp.close()
        print "Update Complete"

if __name__ == "__main__":
    site=website()
    options={1:get_movie_name,2:refresh}
    chosen=int(raw_input())
    options[chosen]()
