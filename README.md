![Stackuchin Logo](https://raw.githubusercontent.com/Rungutan/stackuchin/master/stackuchin-logo.png) 

## What is Stackuchin?

It's a CLI tool developed by [Rungutan](https://rungutan.com) and designed to automatically create, update and delete CloudFormation stacks in multiple AWS accounts and regions at the same time.


## Why use the CLI?

This CLI has been designed for:
1) versioning AWS CloudFormation parameters in GIT
2) deploying to multiple AWS accounts or AWS regions either in PARALLEL or SEQUENTIAL
3) send notifications to Slack channels with AWS errors based on operation
4) support **create**, **update** and **delete** commands
5) can be ran either manually or through a pipeline definition in your CI/CD system
6) supports parent/child stacks
7) it supports NoEcho parameters
8) it supports tagging of resources at stack level
9) it supports unattended deployment (through a CI/CD system)
10) it supports both JSON and YAML versions of AWS CloudFormation

And this is just the tip of the iceberg...

## What can this CLI NOT do?

Unfortunately, it cannot understand contracted forms of verbs in AWS CloudFormation when using YAML templates.

In short, if your AWS CF templates written in YAML use stuff like `!If`, then you have to update them to use their respective version -> `Fn::If`.

## Is it production ready?

We, at [Rungutan](https://rungutan.com), in order to support global concurrency for load testing and ensure high availability as well, have around 200 stacks on average deployed in each and every of the 15 regions our platform currently supports.

In short, yes, we use **Stackuchin** to handle updates for around 3000 AWS CloudFormation stacks.

And no, we're not exagerating or bumping the numbers :-)

## What are the normal use cases?

If simply the fact that you can now git-version all your stacks AND their stack parameters, isn't enough, then:
* your developers can now manage AWS CloudFormation stack themselves, WITHOUT needing to have any "write" IAM permissions
* you can use CI/CD for automated deployments
* you can use pull requests to review parameter/stack changes

## How to install the CLI?

```shell script
pip install stackuchin
```

## How to run the CLI?

* Check the overall help menu

```shell script
$ stackuchin help

usage: stackuchin <command> [<args>]

To see help text, you can run:
    stackuchin help
    stackuchin version
    stackuchin create --help
    stackuchin delete --help
    stackuchin update --help
    stackuchin pipeline --help

CLI tool to automatically create, update and delete AWS CloudFormation stacks in multiple AWS accounts and regions at the same time

positional arguments:
  command     Command to run

optional arguments:
  -h, --help  show this help message and exit

```

* Check the help menu for a specific command

```shell script
$ stackuchin create --help

usage: stackuchin [-h] [--stack_file STACK_FILE] --stack_name STACK_NAME [--secret Parameter=Value] [--slack_webhook SLACK_WEBHOOK] [--s3_bucket S3_BUCKET] [--s3_prefix S3_PREFIX] [-p PROFILE]

Create command system

optional arguments:
  -h, --help            show this help message and exit
  --stack_file STACK_FILE
                        The YAML file which contains your stack definitions.
                        Defaults to "./cloudformation-stacks.yaml" if not specified.
  --stack_name STACK_NAME
                        The stack that you wish to create
  --secret Parameter=Value
                        Argument used to specify values for NoEcho parameters in your stack
  --slack_webhook SLACK_WEBHOOK
                        Argument used to overwrite environment variable STACKUCHIN_SLACK.
                        If argument is specified, any notifications will be sent to this URL.
                        If not specified, the script will check for env var STACKUCHIN_SLACK.
                        If neither argument nor environment variable is specified, then no notifications will be sent.
  --s3_bucket S3_BUCKET
                        Argument used to overwrite environment variable STACKUCHIN_BUCKET_NAME.
                        If argument is specified, then the template is first uploaded here before used in the stack.
                        If not specified, the script will check for env var STACKUCHIN_BUCKET_NAME.
                        If neither argument nor environment variable is specified, then the script will attempt to feed the template directly to the AWS API call, however, due to AWS CloudFormation API call limitations, you might end up with a bigger template in byte size than the max value allowed by AWS.
                        Details here -> https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cloudformation-limits.html
  --s3_prefix S3_PREFIX
                        Argument used to overwrite environment variable STACKUCHIN_BUCKET_PREFIX.
                        The bucket prefix path to be used when the S3 bucket is defined.
  -p PROFILE, --profile PROFILE
                        The AWS profile you'll be using.
                        If not specified, the "default" profile will be used. 
                        If no profiles are defined, then the default AWS credential mechanism starts.

```

## How do you actually use it ?

The logic of the app is simple:
1) Specify the operation that you want to perform
2) Specify the file which contains the parameters for your stack
3) (optional) Add any secrets (aka NoEcho parameters) that your stack might need

Here's the most basic simple definition of a "stack file":
```shell script
your-first-stack:
  Account: 123112321123
  Region: us-east-1
  Template: cloudformation-template.yaml
  # All parameters except NoEcho.
  Parameters:
    paramA: valA
  Tags:
    Environment: UTILITIES
    Team: DevOps
    MaintainerEmail: support@rungutan.com
    MaintainerTeam: Rungutan

another-stack-name:
  Account: 123112321123
  Region: us-east-1
  Template: some-folder/cloudformation-some-other-template.yaml
  # Stack without readable parameters.
  Parameters: {}
  Tags:
    Environment: UTILITIES
    Team: DevOps
    MaintainerEmail: support@rungutan.com
    MaintainerTeam: Rungutan
```

## Running it as a pipeline

```shell script

cat > input.yaml <<EOL

pipeline:
  update:
    - stack_name: TestUpdateStack
  delete:
    - stack_name: TestDeleteStack
  create:
    - stack_name: TestCreateStack
      secrets:
        - Name: SomeSecretName
          Value: SomeSecreValue
EOL

stackuchin  pipeline --pipeline_file input.yaml

```

## Get alerts in Slack

Use the environment variable `STACKUCHIN_SLACK` or the argument `--slack_webhook` to specify a Slack incoming webhook to push your alerts.

You get notified **ALL** with **PROPER MESSAGES**, so that you wouldn't need to have to open your AWS Console to fix your stuff.

Here's a sample:

![Stackuchin Alerts](https://raw.githubusercontent.com/Rungutan/stackuchin/master/stackuchin-alert.png) 


## Running it in a CI/CD process

Here's a sample pipeline that uses our official Docker image to run it in using GitLab CI/CD:

```shell script
image: rungutancommunity/stackuchin:latest

stages:
  - deploy_updates

variables:
  AWS_DEFAULT_REGION: us-east-1
  STACKUCHIN_SLACK: https://hooks.slack.com/services/some_slack_webhook
  STACKUCHIN_BUCKET_NAME: some-deployment-bucket-in-us-east-1
  STACKUCHIN_BUCKET_PREFIX: some/prefix/this/is/optional

deploy_updates:
  only:
    refs:
      - master
  stage: deploy_updates
  script:
    - |
        cat > pipeline.yaml <<EOF
        pipeline:
          pipeline_type: parallel
          update:
            - stack_name: My-First-Stack
            - stack_name: My-Second-Stack
        EOF
    - stackuchin pipeline --stack_file stack_file.yaml --pipeline_file pipeline.yaml
```


## Notes

* If you don't specify a value for a specific stack parameter, then the script will automatically:
1) Set the value as "True" for "UsePreviousValue" (as per AWS documentation), which works just fine for UPDATE and DELETE commands, but of course won't work for CREATE commands
2) If the parameter was not previously defined (aka you're running a CREATE command), it uses (as per AWS Documentation as well) the "Default" value of the parameter as defined in your stack's cloudformation template

* Using secrets (NoEcho) parameters

Defining them as parameters kinda defeats their purpose of being secret.

You should specify them through the `--secret` argument for simple commands, or through the `secrets` property in pipelines.

* The pipeline, if "sequential", will execute the following operations in order:
You can specify only 1, 2 or 3 types of operations mentioned above, but regardless of their order, the script will forcefully process them as:
1) CREATE
2) UPDATE
3) DELETE 

* The pipeline, if "parallel", will execute ALL operations at the same time.

* Due to AWS CloudFormation limitations, a template cannot be supplied as string to the API call if it goes over a certain value in bytes.

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cloudformation-limits.html

For that, you can use the arguments `--s3_bucket` / `--s3_prefix` (or their respective environment variable equivalents`STACKUCHIN_BUCKET_NAME` / `STACKUCHIN_BUCKET_PREFIX`) to specify an intermediate place where to upload the cloudformation template before using it in the API call.

The command will work without supplying these values, but it is recommended that you use them so that you don't encounter any non-necessary errors.