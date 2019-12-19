# Training

Training on AWS with the provided dataset should take less than 15 minutes and cost roughly $0.60. If you add more images or add new labeling classes the cost and time will be higher.
#### Opening the AWS Console
1. Open [AWS Educate](https://aws.amazon.com/education/awseducate/). Log in to your account.
2. Open up your Classroom. ![classroom](classrooms.png)
3. Accept the Terms and Conditions, if presented.
4. Go to your classroom, and click continue. ![openclassroom](open-classroom.png)
5. Open the AWS Console. ![console](aws-console.png)

#### Training with AWS

1. Search "SageMaker" in the "Find Services" field, ![sage](search-sagemaker.png) and create a new notebook instance ![instance](create-instance.png) ![search](create-notebook.png) The notebook instance should have the following characteristics:
 ![newnotebook](new-notebook.png)
 - Notebook instance name: Give your notebook a name
 - IAM Role: Click `Create a new role` inside of the dropdown. Let it have access to Any S3 bucket.
 - Git repositories: open the panel, then click on where it says `None`. Click `Clone a public Git repository to this notebook instance only`, then paste in this link: [https://github.com/wpilibsuite/CoralSagemaker.git](https://github.com/wpilibsuite/CoralSagemaker.git)
 - Create the instance
2. After several minutes, the notebook will be "In Serivce". Open the notebook using the JupyterLab option. ![jupyterlab](open-jupyter.png)
3. Open the `CoralSagemaker` folder, and then `coral.ipynb`, found on the left side of the screen. We've noticed that the first time a notebook is opened, it doesn't work correctly. To fix this, follow these steps:
   - Reload the tab. Dismiss the error. When prompted, select the kernel `conda_amazonei_tensorflow_p36`
   - If the tab does not finish reloading, close the tab, and open the notebook in JupyterLab once again. It will work this time.
4. If you created your own dataset by following the [Gathering](gathering.md) steps, then change the last line of the code to use your data. You must replace `estimator.fit(s3://wpilib)` with `estimator.fit(s3://<<your-bucket-name>>)`. As a reminder, there should be only one `.tar` in your bucket.
5. Run the code block by clicking the play button at the top of your screen. This block will take roughly 15 minutes or less to train your model.
6. Stop the notebook after you are done running it to stop getting charged. Do this by going back to the SageMaker tab, clicking on `Notebook instances` on the far left, selecting the instance that is no longer needed, and selecting `Actions -> Stop`. ![stop](stop-instance.png)
7. Open `Training jobs` on the far left. Open the most recent job.
8. Once the model is done training (the job says `Completed`), scroll to the bottom inside the training job. Click on the link in the `Output` section, where it says `S3 model artifact`.
9. Click on `model.tar.gz`. Click on `Download`.

## [Continue to Inference](inference.md)