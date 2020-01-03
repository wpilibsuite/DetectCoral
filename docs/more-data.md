# Adding Your Own Data to Supervisely
These steps detail how to record a new video, upload it to Supervisely, and label the frames.

### Record a video to label
1. Prepare to record a video of objects you want your robot to detect. You will want to get multiple angles and locations of the objects.
2. Plug a USB Camera into your laptop, point the camera at your chosen object, and run [record_video.py](../utils/record_video.py), which records an MP4. This script records small (640x480) images.
3. Click on the workspace, then the WPILib project that you imported in the [Setting Up Your Data steps](supervisely.md).
4. Upload your own video to your workspace. Click 'UPLOAD' when inside of your workspace, change your import plugin to video, drag in your video, give the project a name, and click import. The default configuration, seen in the picture below, is fine.<br> 
![upload](supervisely-custom-upload.png)
5. Click into your newly import Dataset. Use the `rectangle tool` to draw appropriate boxes around the objects which you wish to label. Make sure to choose the correct class while you are labelling. The class selector is in the top left of your screen. ![labeling](supervisely-labeling.png)

You are now ready to upload your new dataset to Amazon Web Services. [Continue here.](s3.md)