file=`cat last_downloaded.txt`
echo "'$file'" | xargs  rm -r
echo deleted : $file 

