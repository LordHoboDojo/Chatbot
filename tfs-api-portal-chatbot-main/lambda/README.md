# Lambda

This README contains information about files in the `lambda` directory.

# Directory Description

The `lambda` directory contains the python source code files that will constitute the AWS Lambda[^1] function assigned to handle fulfillment of the Amazon Lex Bot found in the `lex` directory. 

Note: if you choose not to set up a Lambda using Python 3.9 and x86_64 architecture, you will need to also include the library files for the `requests` python module which is no longer included in the Lambda Python SDK by default (see instructions here[^2]).

# File Descriptions

File | Description 
--|--
[`constants.py`](/lambda/constants.py) | Defines constants that will be used by `lambda_function.py`.
[`lambda_function.py`](/lambda/lambda_function.py) | Lambda function source code. Handles intent fulfillment for the Lex bot.
[`TFSAPIBotFulfillment-Python3.9.zip`](/lambda/TFSAPIBotFulfillment-Python3.9.zip) | Exported Lambda function with all necessary Python files & `requests` module files already included (Python version 3.9, x86_64 architecture). 

# Setup

There are two methods to set up this lambda function.

## Quick Setup - Python 3.9 Runtime on x86_64 Architecture 

1. If you want to run the Lambda function in a Python 3.9 runtime with x86_64 architecture, then simply go to the AWS Lambda Console > Create Function. Fill out the function name and configuration information as needed (make sure to set the architecture to `x86_64`). 
2. Next, on the Lambda Function console for your newly created function, scroll down to the "Code source" tab and select "Upload from". Choose the ".zip" option and upload the `TFSAPIBotFulfillment-Python3.9.zip` file. Once uploaded, configure a sample test event following the Lex input as defined in the AWS Lex documentation[^3] to ensure that the Lambda function works correctly.
3. Go to the Configuration > Environment Variables page of the Lambda function. There, enter the domain of the [Elastic Beanstalk](/elastic_beanstalk) server, append `/batchSearch` to that domain, and save that value under the environment variable named `BEANSTALK_QUERY_URL` (this can be set to whatever name as long as that change is reflected in `constants.py`).

_**Important**: if you do not have the Elastic Beanstalk server set up yet, please visit its associated [README](/elastic_beanstalk) to see the steps to set it up first. Return to this process once the server has been set up._

4. Finally, to assign the Lambda function to a Lex bot, see instructions here[^3] or visit our Lex directory [README](/lex).

## Other Python Version or Architecture

1. Follow instructions here[^2] to include all library files for the `requests` module. Place the Python source files at the same directory as where the `requests` files are located. Then, compress (zip) all files into a `.zip` archive. 

_**Important**: make sure the Python version of the `requests` (ex: 3.9.x) module matches the Python version of the AWS Lambda function set in the Lambda Console (ex: 3.9)._

2. Next, in the AWS Lambda Console, create a new Lambda function if not already there. Open the Lambda function's dashboard. There should be an "Upload from" dropdown menu on the "Code source" tab of the dashboard. Upload the `.zip` archive containing all the files here.
3. Finally, go to the Configuration > Environment Variables page of the Lambda. There, enter the domain of the [Elastic Beanstalk](/elastic_beanstalk) server, append `/batchSearch` to that domain, and save that value under the environment variable named `BEANSTALK_QUERY_URL` (this can be set to whatever name as long as that change is reflected in `constants.py`).

_**Important**: if you do not have the Elastic Beanstalk server set up yet, please visit its associated [README](/elastic_beanstalk) to see the steps to set it up first. Return to this process once the server has been set up._

4. To assign the Lambda function to a Lex bot, see instructions here[^3] or visit our Lex directory [README](/lex).

#### Footnotes

[^1]: "Lambda Documentation," *Amazon Web Services*. Available [online](https://docs.aws.amazon.com/lambda/).
[^2]: Cziegler, "Using the requests library in AWS Lambda," October 23, 2020. Available [online](https://medium.com/@cziegler_99189/using-the-requests-library-in-aws-lambda-with-screenshots-fa36c4630d82).
[^3]: "Using an AWS Lambda function," *Amazon Web Services*. Available [online](https://docs.aws.amazon.com/lexv2/latest/dg/lambda.html).
