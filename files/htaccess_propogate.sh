find . -type d -exec cp -f ./.htaccess {} \;
find . -type d -exec cp -f ./header.html {} \;
find . -type d -exec zip -r {}/all_files.zip {} \;
find . -type d -exec sed "s/#$%%$#/test/" {}/header.html \; 
