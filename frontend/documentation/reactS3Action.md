# Deploy a React App to Amazon S3 using GitHub Actions

## What this instruction entails:
* Creating an Amazon S3 Bucket
* How to set up the S3 bucket for Web Hosting
* How to configure GitHub Actions to deploy changes automatically

## Create Amazon S3 Bucket
1. Log in the AWS account
2. On the AWS Management Console click __S3__ under the __Storage__ section
3. On the Amazon S3 page, click on the __Create Bucket__ button
4. Provide a __Bucket Name__ (Must be unique)
5. _Note: Check and confirm the __Region__ you are creating the bucket in (US West (Oregon) us-west-2 etc..)_
6. Uncheck the box for __Block all public access__
7. Click the __Next__ button and __Review__ any/all configurations.
8. Click on the __Create Bucket__ button

####  Bucket Policy
_The following Bucket policy instruction is only __IF__ you want the contents of the bucket publicly available, though __NOT__ recommended_
1. Under Buckets, select your bucket name.
2. Choose __Permissions__
3. Choose __Bucket Policy__
4. Copy and modify this simple policy and paste in the editor:

~~~~
{
    "Version": "2012-1-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::<bucket-name>/*"
            ]
        }
    ]
}
~~~~

## Enable Static Web Hosting
1. While in the bucket in AWS under the __Properties__ tab click on the "__Use this bucket to host a website__" radio button.
2. Type "__index.html__"  in the Index document field and Save.

_Note: Confirm the Endpoint, the website will be accessible in the browser using this URL_"

__* At this point, if not already, the gitHub Rpository should be created along with the React app pushed to the repo *__

#### On the GitHub Repo:
1. Click on the __Settings__ Tab.
2. Select __Secret__ on the left side menu
3. Click on __New Secret__ to add a secret providing _Name_ and _Value_:


| Name:          | Value:         |
|:---------------|:---------------|
|AWS_ACCESS_KEY_ID| your-aws-acess-key-id |
|AWS_SECRET_ACCESS_KEY| your-aws-secret-access-key |
|AWS_REGION| us-west-2 or other region |
|AWS_PRODUCTION_BUCKET_NAME| your-aws-bucket|

### Setup GitHub Actions
1. While In the Github repo, click on the __Actions__ tab.
2. On the __Actions__ page, click on the "__Set up this workflow__" or __Set up a workflow yourself__ button. _This takes you to a new page with a web editor with some container code which can be copied and deleted_
3. Copy this container code for the next step.

### Return to your working Branch
1. Create a `.github` folder
2. In the `.github` folder create another folder named `workflows`
3. while in the `workflows` create a `.yml` file with a name that describes the action (example `S3-deploy.yml`)
4. Paste the filler `.yml` provided by GitHub
5. Make the following adjustments to the `.yml` file:
~~~~
name: S3-deploy

on:
  push:
    branches:
      - "development"
      - "reactS3Deploy"
  pull_request:
    branches:
      - "development"
      - "reactS3Deploy"

jobs:
  build:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [15.x]

    steps:
      - uses: actions/checkout@v1
      - run: npm install
        working-directory: ./frontend/floop_feedback
      - run: npm install mini-css-extract-plugin@~2.4.5
        working-directory: ./frontend/floop_feedback
      - run: npm run build
        working-directory: ./frontend/floop_feedback
      - uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-region: ${{ secrets.AWS_REGION }}
          aws-production-bucket-name: ${{ secrets.AWS_PRODUCTION_BUCKET_NAME }}
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          SOURCE_DIR: 'build'
      - name: Deploy app build to S3 bucket
        working-directory: ./frontend/floop_feedback
        run: aws s3 sync ./build s3://${{ secrets.AWS_PRODUCTION_BUCKET_NAME }}
~~~~

The file is made of 3 different parts to help with the understanding:
* __name:__  The name of the Workflow
* __on:__ what triggers the Workflow, in this case the workflow will run anytime you __push__ code to the required __development branch__. _(It will trigger again when pushed to __master__ but no code will be directly pushed to __master__ in this specific project)_
* __jobs:__ Workflow run making up one or more jobs and they run parallel by default:
    * __steps:__ A job contains a sequence of tasks.. Steps run commands nad actions in your repo.
    * __actions/checkout@v2:__ Checks out the repo so workflow can access it.
    * __aws-actions/configure-aws-credentials@v1:__ This configures AWS credentials & region environment for use in other GitHub Actions
    * __Build React App:__ Installs node packages and runs the build in the __package.json__ file, and creates a __build__ folder in the root directory.
    * __Deploy app build to S3 bucket:__  This deploys the newly created build to S3 bucket _bucket-name_ (replace with the name of the created S3 bucket) 

## You should be all set!!

#### Need more help?  
Visit the following helpful named resources and references
* [Better Programming](https://betterprogramming.pub/how-to-deploy-a-reactjs-website-on-aws-s3-with-github-ci-f0519d120063) 
* [S3 Sync GitHub Page](https://github.com/marketplace/actions/s3-sync)
* [DEV Community](https://dev.to/nobleobioma/deploy-a-react-app-to-amazon-s3-using-github-actions-51e)
* [Medium](https://medium.com/trackstack/deploying-a-react-app-to-aws-s3-with-github-actions-b1cb9ba75c95)