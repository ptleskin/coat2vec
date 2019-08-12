# 	download, resize and save wikimedia image to local folder
CONVERTCOMMAND='/usr/local/bin/convert'
$CONVERTCOMMAND $1 \
	-resize $2! -background white -alpha remove \
	-colorspace sRGB -type truecolor $3