#event rules
#event target
#sqs queue
#subscriber
#event sources
from boto3 import client
from common.aws_resources import SQSClass,LambdaClass,EventBridgeClass

#TODO
#move creation actions to tf
def event_setup(
        sqs_config: dict,
        event_rule_config: dict,
        event_target_config: dict,
        lambda_config: dict
        ) -> str:
    """
      setup event resources
    """
    sqs_client = SQSClass(sqs_client=client('sqs'))
    eb_client = EventBridgeClass(eb_client=client('eventbridge'))
    lambda_client = LambdaClass(lambda_client=client('lambda')) 
    #create sqs queue
    queue = sqs_client.create_sqs_queue(
        queue_name=sqs_config['queue_name'],
        tags= sqs_config['tags'] | {},
        attr=sqs_config['attr'] | {}
    )
    #create event rule
    event_rule = eb_client.create_event_rule(
      event_rule=event_rule_config['rule_name'],
      tags=event_rule_config['tags'] | [],
      event_bus=event_rule_config['event_bus'] | 'default'    
    )
    #create targets
    eb_client.create_targets(
        targets=event_target_config['targets'], #queue arn
        event_bus=event_target_config['event)bus'] | "default",
        event_rule=event_rule
    )
    #lambda mapping
    resp = lambda_client.create_event_src_mapping(
        event_src_arn=queue,
        mapping_config=lambda_config     
    )
    print(f"event mapping identifier {resp['UUID']}")
    return resp['UUID']