# Music-Meltdown

   Are u a music lover ?.Ever faced trouble in downloading <strong> tamil </strong> songs ?.Then Music-Meltdown is what you need
   

<h3>Modules to be installed</h3> 
     fuzzywuzzy:https://pypi.python.org/pypi/fuzzywuzzy<br>
     requests:https://pypi.python.org/pypi/requests
  
<br><h3>How  to  setup ?</h3><br>
   1 . Change the song_dir variable in line 6 of the main.py to the directory where songs have to be saved
```
song_dir = "path/to/folder/"
```
2 . Run
```
python main.py
```
3 . Two options are displayed . In order to download continue with the first option . The second option is called <strong> Refresh</strong> . This refresh option updates your local repository (movie.txt).This keeps your local repository upto date. So Its necessary to run this periodically.<strong>You cant download songs of a movie which is not updated in the local repository</strong><br><br>
4. Either you mistype the movie name or type only partial of the movie name.You are provided with list of suggestions which matches with the  movie name. You are free to choose whichever suggested album you wanted to download 

<h4>U are ready to go now !!!!!<h4>
 
 <h3>New updates</h3>
 <ul>
   <li>Now you can delete the last album downloaded . Just run
      
```
  remove.sh

```
   <li>When you hit refresh option , New repositories updated are also shown. So you will so be aware of the newest albums released.
 </ul>
