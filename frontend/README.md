# Video-Object-Segmentation-STCNN

Final project for EECS E6893 Big Data Analytics @ Columbia.
 

## Front-end part

- Django framework:
  Start with python manage.py runserver 
  Open with 127.0.0.1:8000/homepage

- Homepage:
  Showing some basic introductions of our project.

- Upload:
  User can upload a video file with a name and a first-mask picture file.

- Video:
  Once a video is uploaded by a user, Django would send request.post to flask api. Api  will get the uploaded video and return the rendered video. User can watch the video and get the information about this rendered video at the video page.

- Visualization:
  Present a 3D scatter plot to describe the overall offset of the position coordinates of the object we are tracking, corresponding to the motion trajectory of the object in the video. X-axis and y-axis represent the horizontal and vertical coordinates of the object. 
Z-axis represents time, in unit of each frame.

-Gallery:
  A gallery presenting all the cached rendered videos in our project.


## Contact

- [Chong Hu](ch3467@columbia.edu)
- [Yanlin Liu](yl4238@columbia.edu)