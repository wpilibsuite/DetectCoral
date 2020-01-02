# DetectCoral

This technology experiment is a way for teams to automatically detect game pieces and other interesting objects with machine learning. It uses Amazon Web Services to train and test, so teams do not need to own especially powerful computers.

This document describes the steps needed to use a provided set of labeled images and make a trained model to deploy on a RasberryPi with a Google Coral. The basic steps are: gather new data, train your model, run inference on a coprocessor, and use that data meaningfully.

## Table of Contents

- [Set up your data in Amazon Web Services](docs/gather.md)

- [Train your model](docs/training.md)

- [Run your model on a Raspberry Pi](docs/inference.md)

- [Use the data from your model](docs/using-data.md)

- [How it all works](docs/how.md)

### Hardware requirement

- Raspberry Pi 3 or newer
- [Google Coral USB Accelerator](https://coral.ai/products/accelerator/)
