# Training

Training on AWS with the provided dataset should take less than 15 minutes and cost roughly $0.60. If you add more images or add new labeling classes the cost and time will be higher.
#### Opening the AWS Console
1. Open [AWS Educate](https://aws.amazon.com/education/awseducate/). Log in to your account.
2. Open up your Classroom. ![classroom](classrooms.png)
3. Go to your classroom, and click continue. ![openclassroom](open-classroom.png)
4. Open the AWS Console. ![console](aws-console.png)

#### Training with AWS

1. Search "SageMaker" in the "Find Services" field, ![sage](search-sagemaker.png) and create a new notebook instance ![instance](create-instance.png) ![search](create-notebook.png) The notebook instance should have the following characteristics:
 - IAM Permissions: Click `Create a new role` inside of the dropdown. It should have access to ANY S3 bucket.
 - GitHub repository: open the panel, then click on where it says `None`. Click `Clone a public repository to this notebook instance only`, then paste in this link: [https://github.com/wpilibsuite/CoralSagemaker.git](https://github.com/wpilibsuite/CoralSagemaker.git) ![newnotebook](new-notebook.png)
 - Create the instance
2. Open the notebook using the JupyterLab option. ![jupyterlab](open-jupyter.png)
3. Open `coral.ipynb`, found on the left side of the screen. We've noticed that the first time a notebook is opened, it doesn't work correctly. To fix this, follow these steps:
   - Reload the tab. When prompted, select the kernel is `conda_tensorflow_p36`
   - The tab will not finish reloading. Close the tab.
   - Open the notebook in JupyterLab once again. It will work this time.
4. Run the first code block, which builds and deploys the necessary dependencies to an ECR image, used by the training instance.
5. Run the second code block, which gets the execution role, used for communication between computers.
6. Run the third code block, which gets the address of the ECR image made in the first step.
7. If you created your own dataset by following the [Gathering](gathering.md) steps, then change the fourth code block to use your data. You must replace `s3://wpilib` with `s3://<<your-bucket-name>>`. As a reminder, there should be only one `.tar` in your bucket.
8. Run the fourth code block. This block will take roughly 45 minutes to train your model.
9. Remember to stop the notebook after you are done running it to stop getting charged
10. Go to the SageMaker main page in the AWS console. Open Training Jobs. Open the most recent job.
11. Once the model is done training (the job says `Completed`), scroll to the bottom inside the training job. Click on the link in the `Output` section, where it says `S3 model artifact`.
12. Click on `model.tar.gz`. Click on `Download`.

## [Continue to Inference](inference.md)