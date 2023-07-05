# TFS API Portal Chatbot

This repository contains the necessary source materials and documentation for the Toyota Financial Servies (TFS) API Portal chatbot. See [About](/README.md#About) for authors and [References](/README.md#References) for sources. 

# Navigation

Directory | Description 
--|--
[`lex`](/lex) | Contains the `.zip` file constructed when exporting a Lex bot from the AWS Console.
[`lambda`](/lambda) | Contains the source code files for the Lambda function.
[`cloudformation`](/cloudformation) | Contains a README detailing how to deploy the bot using AWS CloudFormation.
[`elastic_beanstalk`](/elastic_beanstalk) | Contains the source code of our Elastic Beanstalk server and necessary index files for our semantic search model.

# Project Abstract

Chatbots have been employed across various industries and applications to improve the experience of end users. With this in mind, our team has developed a chatbot to improve the search experience of developers and business users of the Toyota Financial Services API Portal. Users will be able to describe what they need from an API to the chatbot as if asking another human. Then, leveraging Amazon Lex’s powerful Natural Language Understanding capabilities and our own semantic search model, the chatbot will break down the user’s statement and find the API that best matches their description. The chatbot will provide a conversational approach to searching that returns more relevant results than a traditional keyword/category search, making the process more productive for TFS developers and business users.

# Building the Project

In order to build the project, please visit each of the 4 component directories and follow the instructions in the READMEs for those directories. Additionally, you will need access to an AWS account provided by your organization. We recommend building the project in this order (step 2 can be temporarily skipped if you only need to test that the Bot builds correctly):
1. [Lex](/lex): Core chatbot functionality
2. [Elastic Beanstalk](/elastic_beanstalk): Server to handle some buisness logic, host the semantic search model 
3. [Lambda](/lambda): Handle fulfillment for the Lex bot, needs to be linked to the Bot in the AWS Lex console
4. [CloudFormation](/cloudformation): Deploy Bot onto the web, generate HTML snippet for integration

# Design & Components

![Project Architecture](https://user-images.githubusercontent.com/90115304/232615692-040d656f-0f90-4498-945e-1ceacdd4268d.png)

###### Figure 1: Project Architecture. *From top to bottom: TFS API Portal Website, AWS CloudFormation, Amazon Lex, AWS Lambda, AWS Elastic Beanstalk, TFS endpoints, txtai Library.*

There are 4 main components involved in the design of this project. We named each one based on the corresponding AWS solution used to implement that component: 
- **Amazon Lex**: house the NLP model, conversation flow management
- **Lambda**: handle fulfillment for the Lex chatbot
- **Elastic Beanstalk**: custom semantic search model, business logic
- **CloudFormation**: deployment onto the web, iframe integration

Each of the components handles a specific task, and together they allow our bot to be functional and accessible to users. Please read the READMEs for each of the directories listed under [Navigation](/README.md#Navigation) for more detailed information on how to build each individual component of the project. In the next several sections, we discuss how we approached the development of each component of the project.

## Amazon Lex

We developed the chatbot's conversational model using Amazon Lex. A Lex chatbot model consists of a collection of *Intents*, where each intent represents the goal or purpose of the user's interaction with the bot (for example, a bot used to book hotel stays may have a 'BookRoom' intent). A single bot can have multiple intents, and each intent consists of the following:
- *Utterances*: sample user input that is used to train the NLP unit of the Lex bot to recognize a specific intent.
- *Slots*: parameters or variables who's values need to be collected by the Lex bot in order to fulfill the intent.
- *Slot Types*: the type (in other words, the possible values) associated with each slot. The Lex bot makes use of this information in addition to utterances to develop training examples for its Natural Language Processing unit.
- *Prompts*: follow-up questions the Lex bot can ask the user to collect missing slots. You can also specify what the expected response from the user may appear as, similar to *Utterances*.
- *Fulfillment*: an Intent is fulifilled when the bot uses the slot values provided by the user to execute the intended action. In many cases, an AWS Lambda function is sufficient to handle the fulfillment for a Lex bot.

For more information on Lex, take a look at the AWS documentation [1].

When we were developing our chatbot, we brainstormed a few possible utterances that a user who is looking for an API that has certain functionality (or that falls under certain categories) may provide to the bot. At first, the number of utterances and variety of utterances we provided were very sparse, so the chatbot had difficulty understanding a wide range of user inputs. Later on, we refined our conversation model by adding many more sample utterances for every combination of our four slot types to cover a wide range of possible inputs. This strategy proved successful in that the chatbot was able to recognize the correct intent very frequently for a wide variety of user input. 

Read more about this component in its associated [README](/lex/README.md).

## Lambda

Once the Lex chatbot was fully developed, we were ready to build all the surrounding infrastructure that allows the bot to be accessible to users. The second item we developed was the AWS Lambda function (see [2] for Lambda documentation) to handle fulfillment of our chatbot's 'FindAPI' intent, which was the main intent we focused on for this project. Several iterations of the Lambda function were developed, and initially all of the business logic was handled within Lambda. We found this to be limiting to our goal of using the user input to find the correct API result, so we ultimately moved all of the business logic (retrieving APIs from TFS's own endpoint, authenticating with TFS, etc, matching the user input to API description, etc.) to a separate Elastic Beanstalk server.

By moving a lot of that excess/adjacent processing and business logic to a separate component, our Lambda function is able to focus on the single task of accepting user input from the Lex bot, passing that input to our server which returns a matching API result, and finally transforming the relevant information back into the format required by Lex.

Read more about this component in its associated [README](/lambda/README.md).

## Elastic Beanstalk
 
As mentioned previously, there was a lot of adjacent business logic and processing that we wanted to move from our Lambda function to a separate component of the project to allow the Lambda function to focus on its main task. To house this logic elsewhere, we made use of AWS Elastic Beanstalk, which offers a straightforward and simplified server deployment process. In particular, we chose to use this solution as it integrates well with Python and the Flask library (see [8]). Our Elastic Beanstalk deployment hosts a Flask server that itself makes use of a trained semantic search model via the txtai library (see [7]) to match user input to various API descriptions. The API descriptions are fetched from the TFS endpoint and used to train the txtai model. This enables our chatbot to return results relevant to user input, which is the key functionality of the chatbot in this project.

Read more about this component in its associated [README](/elastic_beanstalk/README.md).

## CloudFormation

To deploy our bot to the web, we made use of AWS CloudFormation (see [3] for documentation). Specifically, we followed the template and instructions provided by AWS (see [6]). By following those steps, we were able to both deploy our chatbot to a standalone website and to integrate it onto the TFS API Portal website via iframe. The CloudFormation template provided by AWS for this Lex Web UI has many parameters that can be configured. The most important parameter is the `WebAppParentOrigin`, which allows the parent website to include the bot as an iframe. If this parameter is not set to the correct URL, the bot will not load on the parent website.

Read more about this component in its associated [README](/cloudformation/README.md).

# References

###### [1] "Amazon Lex Documentation," *Amazon Web Services*. Available [online](https://docs.aws.amazon.com/lex/).
###### [2] "Lambda Documentation," *Amazon Web Services*. Available [online](https://docs.aws.amazon.com/lambda/).
###### [3] "CloudFormation Documentation," *Amazon Web Services*. Available [online](https://docs.aws.amazon.com/cloudformation/).
###### [4] "Elastic Beanstalk Documentation," *Amazon Web Services*. Available [online](https://docs.aws.amazon.com/elastic-beanstalk/).
###### [5] Cziegler, "Using the requests library in AWS Lambda," October 23, 2020. Available [online](https://medium.com/@cziegler_99189/using-the-requests-library-in-aws-lambda-with-screenshots-fa36c4630d82).
###### [6] "AWS Lex Web UI," *Amazon Web Services*. Available [online](https://github.com/aws-samples/aws-lex-web-ui).
###### [7] "txtai: Semantic search and workflows powered by language models," *NeuML*. Available [online](https://neuml.github.io/txtai/).
###### [8] "Flask: web development, one drop at a time," *Pallets*. Available [online](https://flask.palletsprojects.com/en/2.2.x/).

# About

This project was developed by students from the University of Texas at Dallas under mentorship of representatives from Toyota Financial Services.

Student Developers:
- Joah George
- Pranay Yadav
- Gabe Vogel
- Shanauk Kulkarni
- Biruk Mamo
- Cameron Wise

TFS Mentors:
- Slobodan Sipcic
- Jeff Nadeau
