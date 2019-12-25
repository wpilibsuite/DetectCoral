### Inference

1. Acquire a Raspberry Pi 3 or newer, and a [Google Coral USB Accelerator](https://coral.ai/products/accelerator/)
![coral](coral.jpg)
2. Go to the training job in SageMaker, scroll to the bottom, and find the output S3 location
3. Download the the tar file in the bucket.
4. Setup your Raspberry Pi by [following this guide](https://docs.wpilib.org/en/latest/docs/software/vision-processing/raspberry-pi/installing-the-image-to-your-microsd-card.html). This will install an operating system and most of the WPILib software that you will use for machine learning.
5. Plug the Coral into the Pi, as shown in the picture above.
5. After successfully imaging your Pi, plug the Pi into your computer over ethernet. Open `http://frcvision.local` and change the file system to writeable. ![write](writeable.png)
6. Switch to the `Application` tab on the left.
7. Upload the previously downloaded `model.tar.gz` to the Pi by selecting the file in the `File Upload` box, and switching on `Extract .zip and .tar.gz files`
![upload-model](upload-model.png)
8. Click upload.
9. [Download the Python script which runs the model here.](https://github.com/wpilibsuite/CoralSagemaker/releases/download/v1/inference.py)
10. Switch the `Vision Application Configuration` to `Uploaded Python File`, as shown below, and upload the downloaded script.
![upload-py](upload-py.png)
10. Real time labelling can be found on an MJPEG stream located at `http://frcvision.local:1182`
11. The information about the detected objects is put to Network Tables. View the **Network Tables** section for more information about usable output.

## [Continue to Using Data](using-data.md)