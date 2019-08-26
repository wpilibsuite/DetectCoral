# WPILib-ML Docs

## How to Use

### Getting Data

WPILib provides thousands of labelled images for this years game, which you can download here. However, you can train with custom data using this notebook as well. The below instructions describe how to gather and label your own data.

1. Plug a USB Camera into your laptop, and run a script similar to [record_video.py](utils/record_video.py), which simply makes an mp4 from the camera stream.
2. Create a [supervise.ly](supervise.ly) account. This is a very nice tool for labelling data.
3. (Optional) You can add other teammates to your Supervise.ly workspace by clicking 'Members' on the left and then 'INVITE' at the top.
4. Choose a workspace to work in, in the 'Workspaces' tab.
5. Upload the official WPILib labelled data to your workspace. [Download the tar here](https://github.com/GrantPerkins/CoralSagemaker/releases/download/v1/WPILib.tar), extract it, then click 'IMPORT DATA' or 'UPLOAD' inside of your workspace. Change the import plugin to Supervisely, then drag in the extracted FOLDER. Then, give the project a name, then click import. ![import](https://github.com/GrantPerkins/CoralSagemaker/blob/master/docs/supervisely-import.png)
6. Upload your own video to your workspace. Click 'UPLOAD' when inside of your workspace, change your import plugin to video, drag in your video, give the project a name, and click import.
7. Click into your newly import Dataset. Use the `rectangle tool` to draw appropriate boxes around the objects which you wish to label. Make sure to choose the right class when you are labelling. The class selector is in the top left of your screen. ![labeling](https://github.com/GrantPerkins/CoralSagemaker/blob/master/docs/supervisely-labeling.png)

### Training

1. Download your datasets from Supervise.ly. Click on the vertical three dots on the dataset, then "Download as", then select the `.json + images` option. ![json and images](https://github.com/GrantPerkins/CoralSagemaker/blob/master/docs/supervisely-download.png)
2. Go to the Amazon Web Services console website, and search S3 in the "Find Services" field. Open S3.
3. Create a new bucket, and make sure it had public read permissions if multiple accounts will be using this data. ![new bucket](https://github.com/GrantPerkins/CoralSagemaker/blob/master/docs/new-bucket.png)
- Once you've made the bucket, go into the bucket, then `Permissions` --> `Access Control List`. Then change the public access to allow `List objects` and `Read bucket permissions`. ![permissions](https://github.com/GrantPerkins/CoralSagemaker/blob/master/docs/bucket-permissions.png)
4. Upload the `.tar` file that you downloaded from Supervisely into the new S3 bucket. Make sure it also has public read permissions if multiple accounts will be using this data. ![upload tar](https://github.com/GrantPerkins/CoralSagemaker/blob/master/docs/upload-tar.png)
5. Open SageMaker, and create a new notebook instance. The instance should have the following characteristics:
 - IAM Permissions: Click `Create a new role` inside of the dropdown. It should have access to ANY S3 bucket.
 - GitHub repository: open the panel, then click on where it says `None`. Click `Clone a public repository to this notebook instance only`, then paste in this link: [https://github.com/GrantPerkins/CoralSagemaker.git](https://github.com/GrantPerkins/CoralSagemaker.git) ![new notebook](https://github.com/GrantPerkins/CoralSagemaker/blob/master/docs/new-notebook.png)
 - Now create the instance
6. Open `coral.ipynb`, found on the left side of the screen. If prompted, the kernel is `conda_tensorflow_p36`
7. Run the first code block, which builds and deploys the necessary dependencies to an ECR image, used by the training instance.
8. Run the second code block, which gets the execution role, used for communication between computers.
9. Run the third code block, which gets the address of the ECR image made in the first step.
10. Change the fourth code block to use your data. If your data is stored in a bucket called `my-bucket1`, then you must replace `"s3://wpilib"` to `"s3://my-bucket1"`. As a reminder, there should be only one `.tar` in your bucket.
11. Run the fourth code block. This block will take roughly 45 minutes to train your model.
12. Go to the SageMaker main page in the AWS console. Open Training Jobs. Open the most recent job.
13. Once the model is done training (the job says `Completed`), scroll to the bottom inside the training job. Click on the link in the `Output` section, where it says `S3 model artifact`.
14. Click on `model.tar.gz`. Click on `Download`.

### Inference

1. Go to the training job in SageMaker, scroll to the bottom, and find the output S3 location
2. Download the the tar file in the bucket, extract it, and get your .tflite file
3. Put the tflite on your Raspberry Pi by plugging in the SD card into your computer and dragging it in to /home/pi
4. Run the python script, using `python3 object_detection.py --model output.tflite`


## Notebook
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
 
 Building and pushing to ECR takes a while. It should.
 
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
