import json
from helpers import get_logger

logger = get_logger("AWS_RESOURCES")
#add aws class methods
class ECRClass(object):
    """
        AWS ECR Resource Class
    """
    def __init__(self, ecr_resource):
        self.resource = ecr_resource 

    # [2] Define a Global class for AWS Resource: Amazon SNS. 
class SNSClass(object):
    """
        AWS SNS Resource Class
    """
    def __init__(self, sns_client):
        self.sns_client = sns_client
    
    def create_topic(self,topic_name:str,attr: dict,tags: dict, dpp: str) -> str:
        """Create S3 Topic"""
        try:
            logger.info("calling creat topic")
            resp = self.sns_client.create_topic(
                Name= topic_name,
                Attributes = attr,
                Tags = tags,
                DataProtectionPolicy = dpp
                )
            return resp['TopicArn']
            #TODO
            #add logging
        except Exception as ex:
            logger.error(f'An error occured {ex}')
            exit()     
    
    def subscribe_topic(self,topic_arn: str,protocol: str,endpoint: str, attr: dict, return_sub_arn=False) -> str:
        """Subscribe to S3 Topic"""
        try:
            logger.info("calling subscribe")
            resp =self.sns_client.subscribe(
            TopicArn = topic_arn,
            Protocol = protocol,
            Endpoint = endpoint,
            Attributes = attr,
            ReturnSubscriptionArn = return_sub_arn
            )
            return resp['SubscriptionArn']
        except Exception as ex:
            logger.error(f'An error occured {ex}')
            exit()

    def publish_topic(self,topic_arn: str,target_arn: str,msg: str,subject: str,msg_attr: dict) -> str:
        """Publish to S3 Topic"""
        try:
            logger.info("Calling publish topic")
            resp = self.sns_client.publish(
            TopicArn = topic_arn                     ,
            TargetArn = target_arn,
            Message = msg,
            Subject = subject,
            MessageAttributes= msg_attr
            )
            return resp['MessageId']
        except Exception as ex:
            logger.error(f'An error occured {ex}')
            exit()

class EventBridgeClass(object):
    """
      AWS EventBridge Class
    """
    def __init__(self, eb_client):
        self.eb_client = eb_client
        pass
    def get_event_bus(self,name:str) -> str:
        """
        Get details of event bus
        """
        try:
            logger.info("Describe event bus")
            resp = self.eb_client.describe_event_bus(
            Name=name
            )
            return resp["Name"]
        except Exception as ex:
            logger.error(f"Unable to get get event bus {name}: {ex}")
            raise

    def send_event(self,events: list) -> None:
        """
           Send events to Eventbridge
        """       
        try:
            logger.info("Calling put events")
            self.eb_client.put_events(
                Entries= events
            )
        except Exception as ex:
            logger.error(f"Unable to send event: {ex}")
            raise
    
    def create_event_rule(self,event_rule: dict,tags: list=[],event_bus: str="default") -> str:
        """
          Create event rule
        """
        #TODO
        #refactor 
        try:
            logger.info("calling put rule")
            response = self.eb_client.put_rule(
            Name=event_rule["name"],
            ScheduleExpression=event_rule["schedule"],
            EventPattern=event_rule["event_pattern"],
            State=event_rule["state"],
            Description=event_rule["description"],
            RoleArn=event_rule["iam_role"],
            Tags=tags,
            EventBusName=event_bus
            )
            return response["RuleArn"]
        except Exception as ex:
            logger.error(f"Unable to create event rule: {ex}")
            raise

    def create_targets(self,targets: list,event_bus: str,event_rule: str) -> None:
        """
          create event targets
        """
        try:
            logger.error("calling put targets")
            resp = self.eb_client.put_targets(
            Rule=event_rule,
            EventBusName=event_bus,
            Targets=targets
            )
            #TODO
            #logging
            if resp:
                logger.warning(f"The targets {targets} could not be created. Reason: {[[reason['TargetId'],reason['ErrorCode'],reason['ErrorMessage']] for reason in resp['FailedEntries']]}")     
        except Exception as ex:
            logger.error(f"Unable to create event targets: {ex}")
            raise

class SQSClass(object):
    """
      AWS SQS Class
    """
    def __init__(self, sqs_client):
        self.sqs_client = sqs_client
    
    def create_sqs_queue(self,queue_name: str,tags: dict={},attr: dict={}) -> str:
        """
            create sqs queue
        """
        try:
            logger.info("Create queue")
            resp = self.sqs_client.create_queue(
            QueueName=queue_name,
            Attributes=attr,
            tags=tags
            )
            return resp["QueueUrl"]
        except Exception as ex:
            logger.error(f"Unable to create sqs queue: {ex}")
            raise

class LambdaClass(object):
    """
    AWS Lambda Class
    """
    def __init__(self,lambda_client) -> None:
        self.lambda_client = lambda_client
    
    def create_event_src_mapping(
            self,event_src_arn: str,
            **mapping_config: dict
            ):
        """
        Create Event Source Mapping
        """
        try:
            logger.info("Calling create event source mapping")
            resp = self.lambda_client.create_event_source_mapping(
            #TODO refactor
            #try block
            Enabled=mapping_config['enabled'],
            FilterCriteria=mapping_config['filter_criteria'],
            Tags=mapping_config['tags'],
            KMSKeyArn=mapping_config['kms_key'],
            Queues=mapping_config['queues'],
            EventSourceArn=event_src_arn,
            FunctionName=mapping_config['func_name']
            )
            return resp
        except Exception as ex:
            logger.error(f"Unable to create event source mapping: {ex}")
            raise

