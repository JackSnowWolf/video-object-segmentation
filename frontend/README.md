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
  Once a video is uploaded by a user, Django would send requests.post to flask api. Api  will get the uploaded video and return the rendered video. User can watch the video and get the information about this rendered video at the video page.

- Visualization:
  Present a 3D scatter plot to describe the overall offset of the position coordinates of the object we are tracking, corresponding to the motion trajectory of the object in the video. X-axis and y-axis represent the horizontal and vertical coordinates of the object. 
Z-axis represents time, in unit of each frame.

-Gallery:
  A gallery presenting all the cached rendered videos in our project.


## Code

- settings.py
  Add Templates Directory URL and Static Directory URL

- urls.py
  Add five html templates url into urlpatterns.

- models.py
  Create a class named by 'Video'. 'Video' includes 'videoname' which has a charfiled for user to input video's name, and 'frame'&'file' which has a filefiled for user to upload first mask file and video file. 

- views.py
  Assign the api url to the variable 'url'.
  When user upload a video in video page using post method, function 'upload' will assign the input value to a video class. Then it will send a requests.post to url with the input videoname and two uploaded files. Next, flask api return the rendered video in the content along with the video information in the headers. Write and save the returned files and headers to a specific path. Finally, render_to_response to the video.html along with the specific paths.
  In other four functions, use render_to_response to redirect to the specific html page directly.

- templates
  Basically use html and javascript to build up five html pages with some functions including video upload, video play, data visualization, etc.

## Contact

- [Chong Hu](ch3467@columbia.edu)
- [Yanlin Liu](yl4238@columbia.edu)