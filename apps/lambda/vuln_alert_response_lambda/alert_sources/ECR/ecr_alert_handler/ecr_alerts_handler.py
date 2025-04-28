#! /usr/bin/python3
"""
license info
"""
from datetime import date, datetime
import json
from boto3 import resource,client
from os import environ
from common.helpers import send_alert_notification, get_logger
from common.aws_resources import SNSClass, ECRClass
from alert_remediation.ecr_remediation import (
                                                tag_repository,
                                                delete_image,
                                                create_lifecycle_policy
                                            )
logger = get_logger(logger_name='ECR_ALERT_HANDLER')
#TODO change ECR_resource refs to ecr_client
#Initialise required aws resources
_ECR_RESOURCE = client("ecr",region_name="eu-west-2")
_SNS_RESOURCE = { "resource" : resource("sns",region_name="eu-west-2"), 
                        "topic_arn" : environ.get("SNS_TOPIC","NONE") }
#initialise aws ecr resource
ecr = ECRClass(_ECR_RESOURCE)  

def ecr_alerts_handler(event):
    '''Handle ECR image scan alerts'''

    #get alert severity counts
    logger.info(f'Getting severity counts')
    finding_data = get_severity_counts(event=event)
    #respond to alert
    try:
    #TODO schema validation
    #remove hardcoded file path
        logger.info("Loading remediation file alert_remediation/ecr_remediation.json")
        with open("alert_remediation/ecr_remediation.json", "r") as file:
            remediation_config = json.load(file)
    except Exception as ex:
        logger.error(f"File could not be opened: {ex}")
    finding_data = respond_to_alerts(finding_data,ecr,remediation_config)
    #initialise aws ecr resource
    sns = SNSClass(_SNS_RESOURCE)

    #send alert notification

    #TODO
    #criteria for selecting which recipient config to use
    #additional data needed (tags, external data)
    print(f"the finding dtata is {finding_data}")
    with open('alert_recipients/templates/email/email_recipient_config.json', 'r') as fl:
        recipient_config = json.load(fl)
    #TODO
    #return a string of alert_recipients
    logger.info(f'Sending alert notifications')
    send_alert_notification(
        finding_data=finding_data,
        recipient_config=recipient_config
        )

#TODO
#refactor for resource types lambda,ec2,s3
#create alert severity counts method
def get_severity_counts(event) -> dict:
    """
        Extract Severity Counts from alert
    """
    logger.info("Extracting details from event")
    #Extract details from event
    detail_type = event["detail-type"]
    region = event["region"]
    accountId = event["account"] 
    image_repo = event["detail"]["repository-name"]
    repo_arn = event["resources"][0]
    print(f"the repo name is {image_repo}")
    image_digest = event["detail"]["image-digest"]
    image_tags = event["detail"]["image-tags"]

    finding_severity_count = event["detail"]["finding-severity-counts"]
    #TODO
    #ignore zero severity
    severity_count_MEDIUM = 0
    severity_count_CRITICAL = 0
    severity_count_HIGH = 0
    logger.info("Getting severity counts")
    #get severity counts
    if("MEDIUM" in finding_severity_count):
        severity_count_MEDIUM = finding_severity_count["MEDIUM"]
    if("CRITICAL" in finding_severity_count):
        severity_count_CRITICAL = finding_severity_count["CRITICAL"]
    if("HIGH" in finding_severity_count):
        severity_count_HIGH = finding_severity_count["HIGH"]
    logger.info("Creating finding data")
    finding_data = {
            "resource-type": "AWS::ECR-Image",
            "account-id": accountId,
           "finding-data": {
                "resource-id": {
                    "repository": image_repo,
                    "image-id": image_digest,
                    "image-tags": image_tags,
                    "repo-arn": repo_arn
                },
                "region": region,
                "detail-type": detail_type,
                "finding-counts": {
                    "critical": severity_count_CRITICAL,
                    "high" : severity_count_HIGH,
                    "medium": severity_count_MEDIUM
                }
            }
        }
      
    return finding_data

#create alert response method
#TODO
#move to alert response class
#add remediation config 
def respond_to_alerts(finding_data: dict, ecr: ECRClass,remediation_config: dict) -> dict:
    """
        Respond to alerts
    """
    logger.info("Responding to alerts")
    accountId = finding_data["account-id"]
    image_repo = finding_data["finding-data"]["resource-id"]["repository"]
    image_digest = finding_data["finding-data"]["resource-id"]["image-id"]
    #TODO check for empty tag
    image_tag = finding_data["finding-data"]["resource-id"]["image-tags"][0]
    image_ids = [{
            'imageDigest': image_digest,
            'imageTag': image_tag
        }]
    severity_counts = finding_data["finding-data"]["finding-counts"]
    #TODO
    #get image accessed and updated info
    #get image primary tag info
    #add paginator
    finding_data["remediation-actions"] = []
    try:
        logger.info("calling describe image")
        resp = ecr.resource.describe_images(
            registryId=accountId,
            repositoryName=image_repo,
            imageIds=image_ids
        )
    except Exception as ex:
        #for testing
        logger.info(f"The image could not be described: {ex}")
    ###Test data
    resp = {
    'imageDetails': [
        {
            'registryId': accountId,
            'repositoryName': image_repo,
            'imageDigest': image_digest,
            'imageTags': [
                image_tag,
            ],
            'imageSizeInBytes': 123,
            'imagePushedAt': datetime(2025, 1, 1),
            'imageScanStatus': {
                'status': 'COMPLETE',
                'description': 'string'
            },
            'imageScanFindingsSummary': {
                'imageScanCompletedAt': datetime(2015, 1, 1),
                'vulnerabilitySourceUpdatedAt': datetime(2015, 1, 1),
                'findingSeverityCounts': {
                    'string': 123
                }
            },
            'imageManifestMediaType': 'string',
            'artifactMediaType': 'string',
            'lastRecordedPullTime': datetime(2015, 1, 1)
        },
    ],
    'nextToken': 'string'
}
    logger.info("getting time delta")
    last_updated = datetime.today() - resp["imageDetails"][0]["imagePushedAt"] 
    last_accessed = datetime.today() - resp["imageDetails"][0]["lastRecordedPullTime"]
    #TODO
    #move to remediation function
    for remediation in remediation_config["remediations"]:
        match list(remediation.keys())[0]:
            case "delete_image":
                logger.info("Applying delete image remediation")
                #TODO
                #change this one, should not iterate
                for count in remediation["delete_image"]["criteria"]["severity_counts"]:
                    if list(count.keys())[0] == "critical" and severity_counts["critical"] > count["critical"]:          
                        #TODO 
                        #for each image tag
                        #move to get_delta function
                        #there should be additional criteria for deletion, such as env test images
                        #check if image has been accessed or updated in 90 days
                        days_accessed_updated = remediation["delete_image"]["criteria"]["accessed_updated_days"]
                        if last_accessed.days > days_accessed_updated or last_updated.days > days_accessed_updated:
                            logger.info("Calling delete image")
                            finding_data = delete_image(finding_data, ecr)
                            print(f"finding after deletion: {finding_data}")
            case "tag_image":
                logger.info("Applying tag image remediation")
                #TODO
                #criteria should be only from remediation config
                #check if there are criticals and highs
                counts = [list(count.keys())[0] for count in remediation["tag_image"]["criteria"]["severity_counts"]]
                if "critical" or "high" in counts:

                    print("Critical high in tag_image")
                    #check if image has been accessed or updated in 30 days
                    days_accessed_updated = remediation["tag_image"]["criteria"]["accessed_updated_days"]
                    #TODO
                    #if days are more 30 but less than 60
                    if last_accessed.days > days_accessed_updated or last_updated.days > days_accessed_updated:
                        tags = remediation["tag_image"]["criteria"]["tags"]
                        logger.info("Calling tag image")
                        finding_data = tag_repository(finding_data,tags,ecr)
                        print(f"finding after tagging: {finding_data}")
            case "create_lc_policy":
                    logger.info("Applying lifecycle policy remediation")
                    #if there are criticals
                    counts = [list(count.keys())[0] for count in remediation["create_lc_policy"]["criteria"]["severity_counts"]]
                    if "critical" in counts:
                        print("Critical in lc_image")
                        #check if image has been accessed or updated in 60 days
                        days_accessed_updated = remediation["create_lc_policy"]["criteria"]["accessed_updated_days"]
                        if last_accessed.days > days_accessed_updated or last_updated.days > days_accessed_updated:
                            try:
                                logger.info("Loading alert_sources/ECR/ecr_alert_handler/lifecycle_policy.json file")
                                with open("alert_sources/ECR/ecr_alert_handler/lifecycle_policy.json", "r") as file:
                                    lc_policy = file.read()
                                logger.info("Calling create_lifecycle_policy")
                                finding_data = create_lifecycle_policy(
                                    finding_data=finding_data,
                                    ecr=ecr,
                                    lc_policy=lc_policy)
                            except Exception as ex:
                               logger.error(f"Excecption {ex}")
                            print(f"finding data after lc policy {finding_data}")
    #
    #RESPONSE ACTIONS
    #delete image immediately
    #but we do not want to delete image immediately since it can cause chaos if it is constantly being pulled
    #OR delete immediately if the vuln is CRITICAL
    #comment out/in as required
    
#message sections
#finding summary
#finding detail
#remediations applied
#actions required and run book
    return finding_data
    #TODO 
    # get full scan findings and create a report
    #send alert notification
    
    #TODO 
    # save event to logging storage such as S3




