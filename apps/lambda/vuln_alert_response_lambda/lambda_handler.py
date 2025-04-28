from alert_sources.ECR.ecr_alert_handler.ecr_alerts_handler import ecr_alerts_handler
import json



def lambder_handler(event,context=None):

    ecr_alerts_handler(event=event)

#for testing
if __name__ == '__main__':
    lambder_handler(
        event= {
    "version": "0",
    "id": "85fc3613-e913-7fc4-a80c-a3753e4aa9ae",
    "detail-type": "ECR Image Scan",
    "source": "aws.ecr",
    "account": "853038574953",
    "time": "2019-10-29T02:36:48Z",
    "region": "eu-west-2",
    "resources": [
        "arn:aws:ecr:eu-west-2:853038574953:repository/my-repository-name"
    ],
    "detail": {
        "scan-status": "COMPLETE",
        "repository-name": "my-repository-name",
        "finding-severity-counts": {
	       "CRITICAL": 10,
	       "MEDIUM": 9
	     },
        "image-digest": "sha256:7f5b2640fe6fb4f46592dfd3410c4a79dac4f89e4782432e0378abcd1234",
        "image-tags": ["my-image"]
    }
}
)