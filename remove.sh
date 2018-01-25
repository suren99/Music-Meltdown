file=`cat lastdownloaded.txt`
echo $file | xargs  rm -r
echo deleted : $file 

