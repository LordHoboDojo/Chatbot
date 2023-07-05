# Amazon Lex

This README contains information about files in the `lex` directory.

# Directory Description

The `lex` directory contains the `.zip` file which represents the AWS Amazon Lex Bot and its configurations. This bot can be imported into your AWS Amazon Lex console. Please review the AWS Amazon Lex documentation[^1] for an overview of the Amazon Lex Console, how to configure your Bot, Bot versions and aliases, and more important knowledge.

Note: this is a Lex V2 bot, not Lex V1.

# File Descriptions

File | Description 
--|--
[`TFSAPIBot-9-KTW9TRGP1M-LexJson.zip`](/lex/TFSAPIBot-9-KTW9TRGP1M-LexJson.zip) | Exported bot configuration that can be imported into the AWS Lex console. 

# Setup

1. Download the `.zip` file onto your local machine.
2. Go to the AWS Amazon Lex Console > Bots page. There should be an "Action" dropdown menu next to the "Create Bot" button. Click on the "Action" dropdown menu and select the "Import" option. From there, upload the `.zip` file to import the Lex bot under the "Input File" section. Fill out the rest of the necessary information such as Bot name, IAM Roles, etc. according to your personal or organization standards.
3. Once you have the Lambda function[^2] and Elastic Beanstalk server[^3] up and running, you can associated the Lambda function with your Lex Bot to complete the Bot's functionality. To do this, go to Amazon Lex Console > Bots > Bot: `<YourBotName>` > Aliases > Alias: `<YourAliasName>` > Languages > English (US). There, you will be able to choose which Lambda function to attach to the Alias.

#### Footnotes

[^1]: "Amazon Lex Documentation," *Amazon Web Services*. Available [online](https://docs.aws.amazon.com/lex/).
[^2]: See Lambda README [here](/lambda/README.md).
[^3]: See Elastic Beanstalk README [here](/elastic_beanstalk/README.md).
