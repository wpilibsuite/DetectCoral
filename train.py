from sagemaker.estimator import Estimator
from sagemaker import get_execution_role

role = get_execution_role()

instance_type = 'ml.m5.xlarge'
algorithm_name = 'wpi-cpu'


"""
Hyperparameters:
    epochs -> int: number of training steps. Training time is proportional to this number. default = 1000
    batch_size -> int: size of a batch of training images. default = 32
    train_max_run -> int: max seconds a training job can run for. default = 43200
"""
hyperparameters = {'epochs': 200,
                   'batch_size': 32}

ecr_image = "118451457254.dkr.ecr.us-east-1.amazonaws.com/{}:latest".format(algorithm_name)

# The estimator object, using our notebook, training instance, the ECR image, and the specified training steps
estimator = Estimator(role=role,
                      train_instance_count=1,
                      train_instance_type=instance_type,
                      image_name=ecr_image,
                      hyperparameters=hyperparameters,
                      train_max_run=43200)

# Change this bucket if you want to train with your own data. The WPILib bucket contains thousands of high quality labeled images.
# s3://wpilib
estimator.fit("s3://wpilib")
