# WPILib-ML Docs

This document describes the steps needed to use a provided set of labeled images and make a trained model to deploy on a RasberryPi with a Google Coral. The basic steps are: gather new data, train your model, and run inference on a coprocessor.

## How to Use

First, download the official WPILib dataset. [Download the tar here.](https://github.com/GrantPerkins/CoralSagemaker/releases/download/v1/WPILib.tar) If you want to add your own images to this dataset go to the **Gathering Data** section below.

### Training

Training on AWS with the provided dataset should take 1-2 hours and cost roughly $0.60. If you add more images or add new labeling classes the cost and time will be higher.
#### Opening the AWS Console
1. Open [AWS Educate](https://aws.amazon.com/education/awseducate/). Log in to your account.
2. Open up your Classroom. ![classroom](docs/classrooms.png)
3. Go to your classroom, and click continue. ![openclassroom](docs/open-classroom.png)
4. Open the AWS Console. ![console](docs/aws-console.png)

#### Training with AWS

1. Search S3 in the "Find Services" field. Open S3. ![search](docs/search-s3.png) An S3 bucket is a cloud storage service provided by AWS which you will be using to store your .tar of labeled images and the trained model after you finish running through this guide.
2. Create a new bucket by giving it a unique name. Hit next and then hit next again without changing anything on the second page. On the third page, make sure it has public read permissions if multiple accounts will be using this data. ![new bucket](docs/new-bucket.png)
- Once you've made the bucket, go into the bucket, then `Permissions` --> `Access Control List`. Then change the public access to allow `List objects` and `Read bucket permissions`. ![permissions](docs/bucket-permissions.png)
3. Upload the `.tar` file that you downloaded from Supervisely into the new S3 bucket. Click "Add files", then select the file, click "Next", then make sure it also has public read permissions if multiple accounts will be using this data. Keep the file properties "Standard", and then click "Upload" ![upload tar](docs/upload-tar.png)
4. Open SageMaker from the AWS console, ![sage](docs/search-sagemaker.png) and create a new notebook instance ![instance](docs/create-instance.png) ![search](docs/create-notebook.png) The notebook instance should have the following characteristics:
 - IAM Permissions: Click `Create a new role` inside of the dropdown. It should have access to ANY S3 bucket.
 - GitHub repository: open the panel, then click on where it says `None`. Click `Clone a public repository to this notebook instance only`, then paste in this link: [https://github.com/GrantPerkins/CoralSagemaker.git](https://github.com/GrantPerkins/CoralSagemaker.git) ![newnotebook](docs/new-notebook.png)
 - Now create the instance
5. Open the notebook using the JupyterLab option, not the Jupyter Option. ![jupyterlab](docs/open-jupyter.png)
6. Open `coral.ipynb`, found on the left side of the screen. If prompted, the kernel is `conda_tensorflow_p36`
7. Run the first code block, which builds and deploys the necessary dependencies to an ECR image, used by the training instance.
8. Run the second code block, which gets the execution role, used for communication between computers.
9. Run the third code block, which gets the address of the ECR image made in the first step.
10. Change the fourth code block to use your data. You must replace `s3://wpilib` with `s3://<<your-bucket-name>>`. As a reminder, there should be only one `.tar` in your bucket.
11. Run the fourth code block. This block will take roughly 45 minutes to train your model.
12. Remember to stop the notebook after you are done running it to stop getting charged
13. Go to the SageMaker main page in the AWS console. Open Training Jobs. Open the most recent job.
14. Once the model is done training (the job says `Completed`), scroll to the bottom inside the training job. Click on the link in the `Output` section, where it says `S3 model artifact`.
15. Click on `model.tar.gz`. Click on `Download`.

## Inference

1. Go to the training job in SageMaker, scroll to the bottom, and find the output S3 location
2. Download the the tar file in the bucket, and extract it. Notice the `output.tflite` file in the new directory. This is your new trained model.
3. Setup your RasberryPI and Google Coral as described below.
4. Plug the Pi's SD card into your computer, and drag `output.tflite` into the directory `SD_CARD:/home/pi`.
5. Eject the SD card, plug it into your Raspberry Pi again, and turn it on. Connect your Pi to an HDMI monitor with a USB keyboard and mouse, or connect via SSH if it is connected to the same network as your computer.
6. Run the python script, using the command `python3 object_detection.py --model output.tflite --team YOUR_TEAM_NUMBER`
7. Real time labelling can be found on an MJPEG stream located at `http://frcvision.local:1182`
8. The information about the detected objects is put to Network Tables. View the **Network Tables** section for more information about usable output.

#### Raspberry Pi Setup
1. [Follow this guide](https://wpilib.screenstepslive.com/s/currentCS/m/85074/l/1027260-installing-the-image-to-your-microsd-card) in order to install the WPILib Raspberry Pi image. This will install an operating system and most of the WPILib software that you will use for machine learning. However, there are a few dependencies.
2. After successfully imaging your Pi, plug the Pi into your computer over ethernet. Open `frcvision.local` and change the file system to writeable. ![write](docs/writeable.png)
3. With the file system now editable, connect your Pi to an HDMI monitor with a USB keyboard and mouse, or connect via SSH if it is connected to the same network as your computer. PuTTY is a good tool for Windows to SSH.
4. After logging in with the username `pi` and the password `raspberry`, first change the default password to protect your Rasberry Pi.
5. Connect your Pi to the internet.
6. Run the following commands to install the proper dependencies used by the Google Coral.
```bash
sudo apt-get update

wget https://dl.google.com/coral/edgetpu_api/edgetpu_api_latest.tar.gz -O edgetpu_api.tar.gz --trust-server-names

tar xzf edgetpu_api.tar.gz

sudo edgetpu_api/install.sh #NOTE: TYPE 'Y' when asked to run at maximum operating frequency

cd ~

wget https://raw.githubusercontent.com/GrantPerkins/CoralSagemaker/master/utils/object_detection.py
```
7. You now have all dependencies necessary to run real-time inference.
8. When shutting down your Raspberry Pi run the command `sudo poweroff`. It is not recommended to simply unplug your Pi.


#### Network Tables
- The table containing all inference data is called `ML`.
- The following entries populate that table:
1. `nb_boxes`     -> the number (double) of detected objects in the current frame.
2. `boxes`        -> a double array containg the coordinates of every detected object. The coordinates are in the following format: [top_left__x1, top_left_y1, bottom_right_x1, bottom_right_y1, top_left_x2, top_left_y2, ... ]. There are four coordinates per box. A way to parse this array in Java is shown below.
```java
NetworkTable table = NetworkTableInstance.getDefault().getTable("ML");
int totalObjects = (int) table.getEntry("nb_boxes").getDouble(0);
double[] boxArray = table.getEntry("boxes").getDoubleArray(totalObjects*4);
double[][][] objects = new double[totalObjects][2][2]; // array of pairs of coordinates, each pair is an object
for (int i = 0; i < totalObjects; i++) {
    for (int pair = 0; pair < 2; pair++) {
        for (int j = 0; j < 2; j++)
            objects[i][pair][j] = boxArray[totalObjects*4 + pair*2 + j];
        }
    }
}
```
3. `boxes_names`  -> a string array of the class names of each object. These are in the same order as the coordinates.


## Details of procedures used above

### Gathering Data

Machine Vison works by training an algorithm on many images with bounding boxes labeling each object you want the algorithm to recognize. WPILib provides thousands of labeled images for the 2019 game, which you can download below. However, you can train with custom data using this guide as well. If you want to just use the provided images from he instructions below describe how to gather and label your own data.

1. Plug a USB Camera into your laptop, and run a script similar to [record_video.py](utils/record_video.py), which simply makes a .mp4 file from the camera stream. The purpose of this step is to aquire images that show the objects you want to be able to detect.
2. Create a [supervise.ly](https://supervise.ly) account. This is a very nice tool for labelling data. After going to the [supervise.ly](https://supervise.ly) website, the Signup box is in the top right corner. Provide the necessary details, then click "CREATE AN ACCOUNT".
3. (Optional) You can add other teammates to your Supervise.ly workspace by clicking 'Members' on the left and then 'INVITE' at the top.
4. When first creating an account a workspace will be made for you. Click on the workspace to select it and begin working.
5. Upload the official WPILib labeled data to your workspace. (Note: importing files to supervise.ly is only supported for Google Chrome and Mozilla Firefox) [Download the tar here](https://github.com/GrantPerkins/CoralSagemaker/releases/download/v1/WPILib.tar), extract it, then click 'IMPORT DATA' or 'UPLOAD' inside of your workspace. Change the import plugin to Supervisely, then drag in the extracted FOLDER.(Note: Some applications create two folders when extracting from a .tar file. If this happens, upload the nested folder.) Then, give the project a name, then click import. ![import](docs/supervisely-import.png)
6. Upload your own video to your workspace. Click 'UPLOAD' when inside of your workspace, change your import plugin to video, drag in your video, give the project a name, and click import. The default configuration, seen in the picture below, is fine. 
![upload](docs/supervisely-custom-upload.png)
7. Click into your newly import Dataset. Use the `rectangle tool` to draw appropriate boxes around the objects which you wish to label. Make sure to choose the right class when you are labelling. The class selector is in the top left of your screen. ![labeling](docs/supervisely-labeling.png)
8. Download your datasets from Supervise.ly. Click on the vertical three dots on the dataset, then "Download as", then select the `.json + images` option. ![json and images](docs/supervisely-download.png)

### Building and registering the container

This code block runs a script that builds a docker container, and saves it as an Amazon ECR image. This image is used by the training instance so that all proper dependencies and WPILib files are in place.

## How it works

### Dockerfile

The dockerfile is used to build an ECR image used by the training instance. The dockerfile contains the following important dependencies:
 - TensorFlow for CPU
 - Python 2 and 3
 - Coral retraining scripts
 - WPILib scripts
 The WPILib scripts are found in /container/coral/


 ### Data
 
 Images should be labelled in Supervisely. They should be downloaded as jpeg + json, in a tar file.
 When the user calls `estimator.fit("s3://bucket")`, SageMaker automatically downloads the content of that folder/bucket to /opt/ml/input/data/training inside of the training instance.
 
 The tar is converted to the 2 records and .pbtxt used by the retraining script by the tar_to_record.sh script. It automatically finds the ONLY tar in the specified folder and extracts it. It then uses json_to_csv.py to convert the jsons to 2 large csv files. generate_tfrecord.py converts the csv files into .record files. Finally, the meta.json file is parsed by parse_meta.py to create the .pbtxt file, which is a label map.
 
 ### Hyperparameters
 
 At the moment, the only hyperparameter that you can change is the number of training steps. The dict specified in the notebook is written to `/opt/ml/input/config/hyperparameters.json` in the training instance. It is parsed by hyper.py, and is used when calling ./retrain_....sh in train.
 
 ### Training
 
 `estimator.fit(...)` calls the `train` script inside the training instance. It downloads checkpoints, creates the records, trains, converts to .tflite, and uploads to S3.
 
 ### Output
 
 The output `output.tflite` is moved to `/opt/ml/model/output.tflite`. This is then automatically uploaded to an S3 bucket generated by SageMaker. You can find exactly where this is uploaded by going into the completed training job in SageMaker. It will be inside of a tar, inside of a .tar. I don't know why yet.
