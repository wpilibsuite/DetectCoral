### Inference

1. Go to the training job in SageMaker, scroll to the bottom, and find the output S3 location
2. Download the the tar file in the bucket.
3. Setup your Raspberry Pi by [following this guide](https://wpilib.screenstepslive.com/s/currentCS/m/85074/l/1027260-installing-the-image-to-your-microsd-card). This will install an operating system and most of the WPILib software that you will use for machine learning.
4. After successfully imaging your Pi, plug the Pi into your computer over ethernet. Open `http://frcvision.local` and change the file system to writeable. ![write](writeable.png)
5. Switch to the `Application` tab on the left.
6. Upload the previously downloaded `model.tar.gz` to the Pi by selecting the file in the `File Upload` box, and switching on `Extract .zip and .tar.gz files`
![upload-model](upload-model.png)
7. Click upload.
8. [Download the Python script which runs the model here.](https://github.com/wpilibsuite/CoralSagemaker/releases/download/v1/inference.py)
9. Switch the `Vision Application COnfiguration` to `Uploaded Python File`, as shown below, and upload the downloaded script.
![upload-py](upload-py.png)
10. Real time labelling can be found on an MJPEG stream located at `http://frcvision.local:1182`
11. The information about the detected objects is put to Network Tables. View the **Network Tables** section for more information about usable output.

## [Continue to Using Data](using-data.md)