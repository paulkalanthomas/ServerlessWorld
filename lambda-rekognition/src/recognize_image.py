from decimal import Decimal

import boto3
import os

DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE", None)
dynamodb = boto3.resource("dynamodb")
dynamodb_table = dynamodb.Table(DYNAMODB_TABLE)


def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    rekognition = boto3.client("rekognition")
    response=rekognition.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':key}})
    textDetections=response['TextDetections']
    print ('Detected text\n----------')
    entireText=""
    for text in textDetections:
            print ('Detected text:' + text['DetectedText'])
            entireText = entireText + text['DetectedText']
            print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            print ('Id: {}'.format(text['Id']))
            if 'ParentId' in text:
                print ('Parent Id: {}'.format(text['ParentId']))
            print ('Type:' + text['Type'])
            print()
    
    dynamodb_table.put_item(Item={"image-id": key,"tag": labels})

