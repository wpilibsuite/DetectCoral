
# Gathering Data
Machine learning works by "learning" what objects are supposed to look like by looking at thousands of pictures, where important objects have boxes drawn around them. WPILib provides a pre-labeled dataset, however you may wish to supplement this dataset. The below steps describe how to do this. If you do not wish to create your dataset, [skip to Training](training.md).

#### Before you start:
When you record your video, if you do not use the provided script, make sure your images are small (640x40 works). Large images have too much unnecessary data, and will take up too much memory.

### Procedure:
1. Prepare to record a video of objects you want your robot to detect. You should get multiple angles of the object, and many locations of the object.
2. Plug a USB Camera into your laptop, point the camera at your chosen object, and run [record_video.py](../utils/record_video.py), which records and MP4.
3. Create a [supervise.ly](https://supervise.ly) account. This is a very nice tool for labelling data. After going to the [supervise.ly](https://supervise.ly) website, the Signup box is in the top right corner. Provide the necessary details, then click "CREATE AN ACCOUNT".
4. (Optional) You can add other teammates to your Supervise.ly workspace by clicking 'Members' on the left and then 'INVITE' at the top.
5. When first creating an account a workspace will be made for you. Click on the workspace to select it and begin working.
6. Upload the official WPILib labeled data to your workspace. (Note: importing files to supervise.ly is only supported for Google Chrome and Mozilla Firefox) [Download the tar here](https://github.com/wpilibsuite/CoralSagemaker/releases/download/v1/MLwpilib.tar), extract it, then click 'IMPORT DATA' or 'UPLOAD' inside of your workspace. Change the import plugin to Supervisely, then drag in the extracted FOLDER.(Note: Some applications create two folders when extracting from a .tar file. If this happens, upload the nested folder.) Then, give the project a name, then click import. ![import](supervisely-import.png)
7. Upload your own video to your workspace. Click 'UPLOAD' when inside of your workspace, change your import plugin to video, drag in your video, give the project a name, and click import. The default configuration, seen in the picture below, is fine.<br> 
![upload](supervisely-custom-upload.png)
8. Click into your newly import Dataset. Use the `rectangle tool` to draw appropriate boxes around the objects which you wish to label. Make sure to choose the right class when you are labelling. The class selector is in the top left of your screen. ![labeling](supervisely-labeling.png)
9. Download your datasets from Supervise.ly. Click on the vertical three dots on the dataset, then "Download as", then select the `.json + images` option. ![json and images](supervisely-download.png)

## [Continue to Training](training.md)