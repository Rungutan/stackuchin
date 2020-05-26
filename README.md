# stackuchin

## What is Stackuchin?

It's a CLI tool developed by [Rungutan](https://rungutan.com) and designed to automatically create, update and delete CloudFormation stacks in multiple AWS accounts and regions at the same time.


## Why use the CLI?

This CLI has been designed for:
1) versioning AWS CloudFormation parameters in GIT
2) deploying to multiple AWS accounts or AWS regions either in PARALLEL or SEQUENTIAL
3) send notifications to Slack channels with AWS errors based on operation
4) support **create**, **update** and **delete** commands
5) can be ran either manually or through a pipeline definition in your CI/CD system
6) supports both AWS normal CloudFormation templates as well AWS SAM templates
7) supports parent/child stacks
8) it supports NoEcho parameters
9) it supports tagging of resources at stack level
10) it supports unattended deployment (through a CI/CD system)

And this is just the tip of the iceberg...

## What can this CLI NOT do?

Unfortunately, it cannot understand contracted forms of verbs in AWS CloudFormation.

In short, you'll have to rename `!If` commands to `Fn::If`.

## How to install the CLI?

```shell script
pip install stackuchin
```

## Is it production ready?

We, at [Rungutan](https://rungutan.com), in order to support global concurrency for load testing and ensure high availability as well, have around 200 stacks on average deployed in each and every of the 15 regions our platform currently supports.

In short, yes, we use **Stackuchin** to handle updates for around 3000 AWS CloudFormation stacks.

And no, we're not exagerating or bumping the numbers :-)