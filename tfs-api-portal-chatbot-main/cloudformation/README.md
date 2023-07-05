# CloudFormation

This README contains information about files in the `cloudformation` directory.

## Directory Description

The `cloudformation` directory contains the instructions necessary to deploy the Amazon Lex chatbot onto the web using AWS CloudFormation[^1]. This enables the chatbot to be accessed by other users, and allows for integration of the chatbot onto another website. All files required are generated when following the steps in this[^2] tutorial.


## Setup

1. Follow one of the guides to integration provided by AWS. The guide on Github[^2] provides multiple solutions to integrating the Lex bot to a UI, but the CloudFormation is the simplest. A more straight-forward guide for integration specifically for CloudFormation can be found on AWS's website[^3]. The guides may tell you to have <b>EnableCognitoLogin</b> to be set to `true`, but this is not required for integration. Make sure the <b>WebAppParentOrigin</b> parameter is a website that you have access to and are able to edit the HTML. Here is a list of parameters to set (all other parameters can be left as default). The value `<blank>` means to delete whatever value is populated by default in that field and leave it blank.

```
CodeBuildName: api-bot-ui
HideButtonMessageBubble: true
LexV2BotAliasId: <YourAliasId>
LexV2BotId: <YourBotId>
retryOnLexPostTextTimeout: true
retryCountPostTextTimeout: 1
ShouldLoadIframeMinimized: true
ShowResponseCardTitle: true
WebAppConfBotInitialSpeech: <blank>
WebAppConfBotInitialText: Hi, I can help you find the API you are looking for. For example, ask me "What API can I use to get vehicle locations?" or "I need an API for user payment management".
WebAppConfNegativeFeedback: <blank>
WebAppConfPositiveFeedback: <blank>
WebAppConfToolbarTitle: API Portal Chatbot
WebAppParentOrigin: <base URL of website the bot will be integrated onto>
WebAppPath: <comma-separated list of paths on the WebAppParentOrigin where the Bot will be located (ex: '/chatbot')>
```

2. After successfully setting up the CloudFormation, the scripts you find in the <b>SnippetUrl</b> of the CloudFormation Stack's "Outputs" tab, should be pasted into the body element of the webpage where you would like the bot to appear. Remember, this webpage must be under the domain you specified in <b>WebAppParentOrigin</b>. Let `cloudfrontURL` be the URL generated in CloudFormation > Stacks > `<YourStackName>` > Outputs > **WebAppDomainName** (prepend `https://` to the domain name if necessary). Then the following is an example of the scripts you will need to include:
  
``` 
    <script src="<cloudfrontURL>/lex-web-ui-loader.js"></script>

    <script>
        var loaderOptions = {
            configUrl: '<cloudfrontURL>/lex-web-ui-loader-config.json',
            baseUrl: 'cloudfrontURL'
        };

        var iframeLoader = new ChatBotUiLoader.IframeLoader(loaderOptions);
        console.log(iframeLoader.config)
        iframeLoader.load()
            .then(function () {
            console.log('iframe loaded');
            })
            .catch(function (err) {
            console.error(err);
            });

    </script>
```

3. The bot should appear in the lower right hand corner of the webpage. If you do not see the bot, inspect the webpage and see if there are any error (you may need to wait a minute for the errors to appear).

#### Footnotes

[^1]: "CloudFormation Documentation," *Amazon Web Services*. Available [online](https://docs.aws.amazon.com/cloudformation/).
[^2]: "AWS Lex Web UI," *Amazon Web Services*. Available [online](https://github.com/aws-samples/aws-lex-web-ui).
[^3]: "Deploy a Web UI for Your Chatbot," *Amazon Web Services*. Available [online](https://aws.amazon.com/blogs/machine-learning/deploy-a-web-ui-for-your-chatbot/).
