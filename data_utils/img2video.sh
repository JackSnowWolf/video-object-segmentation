#!/bin/bash
ffmpeg -f image2 -i /media/huchong/Entertainment/DAVIS/JPEGImages/480p/bear/%05d.jpg -c:v libx265 -preset medium -crf 18 -r 24 bear.mp4
