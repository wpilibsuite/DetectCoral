# Training

Training on AWS with the provided dataset should take less than 15 minutes and cost roughly $0.60. If you add more images or add new labeling classes the cost and time will be higher.
#### Opening the AWS Console
1. Open [AWS Educate](https://aws.amazon.com/education/awseducate/). Log in to your account.
2. Open up your Classroom. ![classroom](docs/classrooms.png)
3. Go to your classroom, and click continue. ![openclassroom](docs/open-classroom.png)
4. Open the AWS Console. ![console](docs/aws-console.png)

#### Training with AWS

1. Search S3 in the "Find Services" field. Open S3. ![search](docs/search-s3.png) An S3 bucket is a cloud storage service provided by AWS which you will be using to store your .tar of labeled images and the trained model after you finish running through this guide.
2. Create a new bucket by giving it a unique name. Hit next and then hit next again without changing anything on the second page. On the third page, make sure it has public read permissions if multiple accounts will be using this data. ![new bucket](docs/new-bucket.png)
- Once you've made the bucket, go into the bucket, then `Permissions` --> `Access Control List`. Then change the public access to allow `List objects` and `Read bucket permissions`. ![permissions](docs/bucket-permissions.png)
3. Upload the `.tar` file that you downloaded (or made with Supervise.ly) into the new S3 bucket. Click "Add files", then select the file, click "Next", then make sure it also has public read permissions if multiple accounts will be using this data. Keep the file properties "Standard", and then click "Upload" ![upload tar](docs/upload-tar.png)
4. Open SageMaker from the AWS console, ![sage](docs/search-sagemaker.png) and create a new notebook instance ![instance](docs/create-instance.png) ![search](docs/create-notebook.png) The notebook instance should have the following characteristics:
 - IAM Permissions: Click `Create a new role` inside of the dropdown. It should have access to ANY S3 bucket.
 - GitHub repository: open the panel, then click on where it says `None`. Click `Clone a public repository to this notebook instance only`, then paste in this link: [https://github.com/wpilibsuite/CoralSagemaker.git](https://github.com/wpilibsuite/CoralSagemaker.git) ![newnotebook](docs/new-notebook.png)
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

## [Continue to Inference](inference.md)