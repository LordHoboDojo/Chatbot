# Elastic Beanstalk

This README contains information about files in the `elastic_beanstalk` directory.

# Directory Description

The `elastic_beanstalk` directory contains the source code of a custom Python-Flask[^1] server which has two main responsibilities:
1. Host the trained semantic search model (trained via the txtai[^2] library).
2. Receive search queries from the Lambda function and return the API that has a best match.

This Flask server is then deployed by AWS Elastic Beanstalk[^3], which then allows the Lambda function to make HTTP calls to the server to retrieve the information it needs to fulfill the chatbot's intent.

# File Descriptions

File | Description 
--|--
[`Elastic_Beanstalk_Server.zip`](/elastic_beanstalk/Elastic_Beanstalk_Server.zip) | This contains all the necessary files needed to import into AWS Elastic Beanstalk console and get the server up and running with a few clicks.
[`flask.txt`](/elastic_beanstalk/flask.txt) | This contains licence for flask
[`txtai.ipynb`](/elastic_beanstalk/txtai.ipynb) | This contains the code to train the model used in the flask server using txtai
[`txtai.txt`](/elastic_beanstalk/txtai.txt) | This contains the licence for txtai

# Setup

## Quick Setup

1. Go to the AWS Elastic Beanstalk console. Create a new Application.
2. Once the Application has been created, in the side navigation bar go to Application: `<YourAppName>` > Application versions. From there, select the "Create Environment" option. 
3. Set the "Environment Tier" to "Web server environment". In the "Platform" section, select "Python". In the "Application Code" section, select "Upload your code" and upload the `Elastic_Beanstalk_Server.zip` file. For the rest of the setup, leave the default values or follow your organization's policies/standards to configure those settings. Click "Submit" at the "Review" step.
4. The Elastic Beanstalk server should be up and running. Monitor its status in the AWS console. The "domain" of the server (available on the environment page for the environment you set up in step 3) will be needed when setting up the [Lambda](/lambda) function.


#### Footnotes
[^1]: "Flask: web development, one drop at a time," *Pallets*. Available [online](https://flask.palletsprojects.com/en/2.2.x/).
[^2]: "txtai: Semantic search and workflows powered by language models," *NeuML*. Available [online](https://neuml.github.io/txtai/).
[^3]: "Elastic Beanstalk Documentation," *Amazon Web Services*. Available [online](https://docs.aws.amazon.com/elastic-beanstalk/).
