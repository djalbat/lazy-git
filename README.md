# Lazy Git

It seems to be well known that GitHub uses [rate limiting](https://developer.github.com/v3/#rate-limiting) for API requests. What is apparently less well known as that it provides a mechanism to mitigate rate limiting, namely [conditional requests](https://developer.github.com/v3/#conditional-requests). For most requests, GitHub will include the time at which the requested resource was last modified in the response in the form of a `Last-Modified` header. If you include this time in subsequent requests for the same resource in the form of a `If-Modified-Since` header, and if the resource has not been modified since, GitHub will return a `304 Not Modified` status code as opposed to the usual `200 OK` status code. In these cases your rate limit is unaffected and you can safely use the previous response, provided of course that you have stored it.

This is all that Lazy Git does, to save you the bother of doing so. You need only point your web application or service at Lazy Git, as opposed to GitHub, and keep everything else the same. Aside from a couple of very minor differences, Lazy Git's response will appear to be identical to the response you would otherwise have gotten from GitHub.

## Caveats

* Only basic HTTP authentication is currently supported. There is no reason why other modes of authentication cannot be supported, please reach out or submit a pull request. Lazy Git itself does not require authentication, however it extracts the tokens in order to store responses in directories unique to users.

* Currently, due to the seeming limitations of Python's Flask framework, chunked transfer encoding is not supported by Lazy Git even though it appears to be the default for GitHub. If this means nothing to you, don't worry about it.

## Status codes

In the unlikely event that GitHub returns a `500 Internal Server Error` status code, like a good proxy Lazy Git will modify this to a `502 Bad Gateway` status code so as to keep the former status code for its own use. Therefore:

1. If you see a `500 Internal Server Error` status code, something is amiss with Lazy Git.

2. If you see a `502 Bad Gateway` status code or indeed any other error code, something is amiss with GitHub.

In the first case, it is likley that Basic HTTP authentication has not been used and therefore Lazy Git has been unable to extract the authorisation token.

In the second case, Lazy Git will leave the remainder of the response intact, including the headers. Therefore it should be possible to work out what has gone awry by inspecting the headers or indeed the body of the response.

## Installing and developing locally

We recommend [Conda](https://conda.io/en/latest/) for a straightforward installation. Assuming that Conda is installed, firstly create and activate a Conda environment:

    conda create --name lazy-git
    conda activate lazy-git

Once the environment is active, install Python and the dependencies:

    conda install python=3.4.3
    conda install --yes --file requirements.txt

Of course you are free to use [Pip](https://pypi.org/project/pip/) instead. The choice of Python version echoes the version of Python 3 currently used in production, by the way.

You also need to install a local version of DynamoDB. Instructions for doing so are given in a separate section that follows.

Before running the application, you need to set up a local environment. There are no configuration files in the distribution, however the following template can be used:

```
export GITHUB_HOST=https://api.github.com

export LOG_LEVEL=DEBUG

export HEALTHCHECK='/'

export SECURITY_MODE='public'

export GITHUB_USERNAME=...
export GITHUB_AUTHORISATION_TOKEN=...

export TABLE_NAME=lazy-git
export REGION_NAME=eu-west-1
export ENDPOINT_URL=http://localhost:8000
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
```

The sensitive information has been left out. You will need to provide a genuine GitHub username and authorisation token, for example. Both the AWS access key identifier and AWS secret access key can be spurious for local development. See the section that follows for further details.

Assuming you have saved the above to a `configuration/local.env` file, the following command will set things up:

    source configuration/local.env

Once this done, you can run the application from the root directory thus:

    python webapp/main.py

And the tests thus:

    pytest

If you want to use PyCharm's EnvFile plugin, remove the `export` keywords from in front of each of the directives.

## Installing and configuring a local DynamoDB instance

Amazon's [DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) is used to cache responses. In order to develop locally and run the tests, therefore, you need to install and configure a local instance of it.

DynamoDB runs on Java. The easiest way to install Java on MacOS is via [Homebrew](https://brew.sh/):

```
brew cask install java
```

Once this is done, following the instructions for downloading and configuring DynamoDB that are given here:

[DynamoDB (Downloadable Version) on Your Computer](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html)

Adjunct to these instructions, the following points may help:

* With DynamoDB running you will not be able to see anything from your browser, with both `http://localhost:8000` and `https://localhost:8000` returning nothing. This is nothing to worry about.

* If you want to check the installation, the best way to do so is to connect via Amazon's CLI tool:

  [What Is the AWS Command Line Interface?](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)

  By far the easiest way to install this on MacOS is with Pip:

  ```
  pip install aws
  ```

* Once you have to tool installed, you should immediately configure it:

  ```
  aws configure
  ```

  Since you are connecting only to your own local DynamoDB instance, you can give spurious values for both the access and secret access keys. The Amazon documentation suggests something along the lines of `fakeAccessKeyId` and `fakeSecretAccessKey`. Also give a region name, `eu-west-1` will do if you can't think of anything else.

  You would think that you would have to configure your DynamoDB instance to accept these keys but this appears not to be the case. Configuring the command line tool simply keeps it happy.

  By the way, this information is stored two files to be found in the hidden `~/.aws` folder. Finally, note that Lazy Git uses its own configuration variables, stored as environment variables. You do not need to change them when running locally for the aforementioned reasons.

* Assuming that you have your DynamoDB instance running, you can test it with the following command:

  ```
  aws dynamodb --endpoint-url http://localhost:8000 list-tables
  ```

* Lazy Git itself uses [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) to connect to DynamoDB. The section of the Boto3 documentation relating to [DynamoDB](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html) might be helpful.

## Contact

* james.smith@glgroup.com
