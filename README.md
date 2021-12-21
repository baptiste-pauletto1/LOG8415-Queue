# LOG8415 : Queue Analysis

Repository of my personnal project in the **LOG8415 : Advanced Concepts of Cloud Computing** class at Polytechnique Montréal.

## Queue analysis (*Analyse de files d'attentes*)

The project's main goal is to get hands on with AWS services like **Lambda functions**, **Simple Notification Service**, **Simple Queue Service** and **DynamoDB**  in order to complete a performance analysis of actual implementation of waiting queues using a serverless approach.

## Architecture

The project architecture on AWS will focus on the components in the main square of this picture.
![Architecture](https://github.com/baptiste-pauletto1/Queue-Analysis/blob/main/architecture.png?raw=true)
<figcaption align = "center"><b>Fig.1 - Project architecture </b></figcaption>

# Project setup

Please follow the next steps in order to run the project on your own machine.
Notice that it requires to have both *awscli* and *Docker* installed on your distribution

## Step 0 : Clone repository
Clone the current repository using your favorite method (HTTPS, SSH...) and place yourself in the freshly cloned repo.

## Step 1 : Build docker image
To build the docker image where the project will run, use the following commands :
```shell
docker build -t <NAME> .
./run_docker.sh
cd python/
```
Notice that you can replace `<NAME>` with the name of your choice, in my case, I will be using `log8415`.

You should now be inside your docker image, ready to run the scenarios.

## Step 2 : Launch scenarios
In order to run the scenarios, you will have to launch one of the following commands depending on what scenario you want to run :

* Baseline :
```shell
python3 baseline.py
```
* Standard Queue :
```shell
python3 scenario_1.py
```
* FIFO Queue :
```shell
python3 scenario_2.py
```
More details about each scenario are present in the `LOG8415_projet.pdf` file.

When running scenarios, different logging steps will be displayed in order to follow how everything is going.

*Notice* : Each scenario file has been thought in a way that allows him to be run independently of other scenario.
That is why, in each scenario, the setup goes from the very start (creating components), to the end (delete each part).

## Step 3 : Launch metrics production

In order to produce relevant metrics, you will have to run the three scenarios, otherwise, some data will not be present in the barplots generated.
Once those three scenarios are done, use the following command:

```shell
python3 metrics.py
```
Resulting barplots will be stored inside the `metrics_result` folder.

## Results

The produced barplot should look like those following :

![Invocation comparison barplot](https://github.com/baptiste-pauletto1/Queue-Analysis/blob/main/metrics_result/invocation_comparison.png?raw=true)
<figcaption align = "center"><b>Fig.1 - Number of invocation comparison</b></figcaption>

![Duration comparison barplot](https://github.com/baptiste-pauletto1/Queue-Analysis/blob/main/metrics_result/duration_comparison.png?raw=true)
<figcaption align = "center"><b>Fig.2 - Average duration comparison</b></figcaption>

![Concurrent comparison barplot](https://github.com/baptiste-pauletto1/Queue-Analysis/blob/main/metrics_result/concurrent_comparison.png?raw=true)
<figcaption align = "center"><b>Fig.3 - Average Concurrent executions comparison</b></figcaption>

## Author

Baptiste Pauletto
