from common.aws_resources import ECRClass
from common.helpers import get_logger

logger = get_logger("ECR_REMEDIATION")

def delete_image(
    finding_data: dict,
          ecr: ECRClass,
        ) -> dict:
    
    '''Delete the image from repository'''
    #TODO
    #add delete criteria: 
    # repo not accessed or updated for 90 days 
    # by tag value
    #severity counts
    try:   
        logger.info("Calling batch delete image")
        response = ecr.resource.batch_delete_image(
            registryId = finding_data["account-id"],
            repositoryName = finding_data["finding-data"]["resource-id"]["repository"],
            imageIds = [
                {
                "imageDigest": finding_data["finding-data"]["resource-id"]["image-id"],
                "imageTag": finding_data["finding-data"]["resource-id"]["image-tags"][0]
                }
            ])       
        #check if deletion was successful
        failure = response["failures"]
        if not failure:
            logger.info("This imageID: %s and Tag: %s have been deleted " \
            "successfully"%( finding_data["finding-data"]["resource-id"]["image-id"],finding_data["finding-data"]["resource-id"]["image-tags"][0]))
            finding_data["remediation-actions"].append(
                {   
                    "action": "delete",
                    "status": "image delete successfully"       
                 }
            )
        else:
            logger.info("Please delete image from repository manually")
            finding_data["remediation-actions"].append(
                {   
                    "action": "delete",
                    "status": "failed to delete image"   
                 }
            )
    except Exception as ex:
        logger.error("The image could not be deleted. Reason: %s"%(ex))
        finding_data["remediation-actions"].append(
                {   
                    "action": "delete",
                    "status": "failed with exception"         
                 }
            ) 
    return finding_data

    #create a lifecycle policy
    #applying a lifecycle policy to the image tag will give the team a 24 hour window to update the image before deletion
def create_lifecycle_policy(
        finding_data: dict,
        ecr: ECRClass,
        lc_policy: str) -> dict:
    '''Attach lifecycle policy to the image'''

    try:
        logger.info("Calling put lifecycle policy")
        ecr.resource.put_lifecycle_policy(
            registryId= finding_data["account-id"],
            repositoryName= finding_data["finding-data"]["resource-id"]["repository"],
            #TODO move rule json into file and ref with variable
            lifecyclePolicyText=lc_policy
            )
        
        logger.info("LifeCycle Policy was created successfuly!!")
        finding_data["remediation-actions"].append(
                {   
                    "action": "create life cycle polcy",
                    "status": "LifeCycle Policy was created successfuly"        
                 }
            ) 

    except Exception as ex:
        logger.exception(f"LifeCycle Policy could not be updated. Reason: {ex}")
        finding_data["remediation-actions"].append(
                {   
                    "action": "create life cycle polcy",
                    "status": "Failed to create LifeCycle Policy with exception"        
                 }
            ) 
    return finding_data

    #tag repository
    #we can tag the repo STATUS to UPDATE-IMAGE-OR-DELETE with do not use or schedule for deletion
    #the team can review the alert and  update the image with latest tag and delete the vulnerable one
    #NOTE this tags the repo not the image so best to include the image tag in the tag Value 

def tag_repository(finding_data: dict,tags: list,ecr: ECRClass) -> dict:

    '''Tag image repository'''
    try:
        logger.info("Calling tag repository")
        tag_response = ecr.resource.tag_resource(
            resourceArn=finding_data["finding-data"]["resource-id"]["repo-arn"],
            #TODO iterate tag list
            tags=[
                {
                    'Key': list(tags[0].keys())[0],
                    'Value': 'UPDATE-OR-DELETE-%s'%(tags[0]["key1"])
                },
            ]
        )       
        if  not tag_response:
            logger.info("Repository Tag was updated successfully!")
            finding_data["remediation-actions"]["resource-tag-status"] = "Repository Tag was updated successfully"
    except Exception as ex:
        logger.error(f"Repository Tag could not be updated. Reason: {ex}")
        finding_data["remediation-actions"].append(
                {   
                    "action": "resource-tag",
                    "status": "Repository Tagging failed with exception"        
                 }
            ) 
    
    return finding_data