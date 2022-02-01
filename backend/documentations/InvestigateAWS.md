# Investigate AWS technology that can clustering algorithm on Dynamo DB data
- Amazon Sage Maker k-means clustering algorithm
- Good clustering in single pass
- Requires update model with time with new proportional data w/ no need to retain data
- Processing a 400-dimensional dataset of 23 M entries (~37 GB of data), with k=500 clusters can be done in 7 minutes
- Although we require a single pass, our algorithm achieves the same mean square distance cost as the state-of-the-art multiple pass implementation of k-means++ (or k-means||) initialization coupled with Lloyds iteration.
- Pricing is based on usage per hours and instance cpu and memory requirements starting at $0.05 an hour for 2 vCPU and Memory of 4GiB.
[K-means clustering with amazon sagemaker](https://aws.amazon.com/blogs/machine-learning/k-means-clustering-with-amazon-sagemaker/)

### Amazon DynamoDB cluster Algorithm:
1. DynamoDB Accelerator (DAX) Clustering is integrated with DynamoDB
2. High Scalability
3. API capable with DynamoDB
4. Can have one cluster for multiple DynamoDB tables or multiple clusters for single DynamoDB table
5. Can launch a DAX cluster in your virtual network and control access to the cluster by using Amazon VPC security groups.
6. Pay by provisioned capacity
[Walkthrough of Amazon Dyanamo DB Accelerator Console Part-2](https://aws.amazon.com/blogs/database/a-walkthrough-of-the-amazon-dynamodb-accelerator-console-part-2/)
---

## Amazon Web Services
### K-means clustering with Amazon SageMaker | Amazon Web Services
> Amazon SageMaker provides several built-in machine learning (ML) algorithms that you can use for a variety of problem types. These algorithms provide high-performance, scalable machine learning and are optimized for speed, scale, and accuracy. Using these algorithms you can train on petabyte-scale data. They are designed to provide up to 10x the performance of the other […]

`Nov 8th, 2018
	https://aws.amazon.com/blogs/machine-learning/k-means-clustering-with-amazon-sagemaker/'

### Amazon Web Services
- A walkthrough of the Amazon DynamoDB Accelerator console – Part 2 | Amazon Web Services
- Amazon DynamoDB provides scalability and performance where response times are measured in single-digit milliseconds. For use cases requiring response times in microseconds, DynamoDB Accelerator (DAX) is the service that helps deliver that. DAX is a managed cache that is API compatible with DynamoDB  providing fast in-memory performance for demanding applications like real-time gaming, bidding, weather […]
*Jul 29th, 2019*

### Amazon Web Services Amazon Web Services
- K-means clustering with Amazon SageMaker | Amazon Web Services
- Amazon SageMaker provides several built-in machine learning (ML) algorithms that you can use for a variety of problem types. These algorithms provide high-performance, scalable machine learning and are optimized for speed, scale, and accuracy. Using these algorithms you can train on petabyte-scale data. They are designed to provide up to 10x the performance of the other […]
*Nov 8th, 2018*
[K means clustering with amazon sagemaker](https://aws.amazon.com/blogs/machine-learning/k-means-clustering-with-amazon-sagemaker/)


### Amazon Web ServicesAmazon Web Services
- A walkthrough of the Amazon DynamoDB Accelerator console – Part 2 | Amazon Web Services
- Amazon DynamoDB provides scalability and performance where response times are measured in single-digit milliseconds. For use cases requiring response times in microseconds, DynamoDB Accelerator (DAX) is the service that helps deliver that. DAX is a managed cache that is API compatible with DynamoDB  providing fast in-memory performance for demanding applications like real-time gaming, bidding, weather […]
*Jul 29th, 2019 (49 kB)*

