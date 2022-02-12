#lambda 1

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event["s3-key"]       ## TODO: fill in
    bucket = event["s3-bucket"] ## TODO: fill in
    
    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket, key, '/tmp/image.png')
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

#----------------------------------------------------------------------------
#lambda 2

import json
import base64
import boto3

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2022-01-23-17-23-37-239"   ## TODO: fill in

runtime = boto3.client("runtime.sagemaker")

def lambda_handler(event, context):
    
    print("Event : ", event)

    # Decode the image data
    #image = base64.b64decode(event["image_data"])      ## TODO: fill in)
    image = base64.b64decode(event['body']['image_data'])
    
    response = runtime.invoke_endpoint(EndpointName = ENDPOINT, ContentType = 'image/png',Body=image)
    
    #inferences =predictor.predict(event["image"]) ## TODO: fill in
    #inferences = json.loads(response["Body"].read())
    inferences = response["Body"].read()
    
    # We return the data back to the Step Function    
    
    event["inferences"] = inferences.decode('utf-8')
    print("Event: ", event)
    print("Inference: ", inferences)
    

    #event["inferences"] = inferences
    return {
          "statusCode": 200,
          "body": json.dumps(event)
    }

#----------------------------------------------------------------------------
#lambda-3

import json


THRESHOLD = .93


def lambda_handler(event, context):

    # Grab the inferences from the event
    #inferences = event['body']['inferences']      ## TODO: fill in
    #body = json.loads(event['body'])
    #inferences = json.loads(event['inferences'])
    
    body = json.loads(event['body'])
    inferences = json.loads(body['inferences'])

    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = any(x > THRESHOLD for x in inferences) ## TODO: fill in

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }