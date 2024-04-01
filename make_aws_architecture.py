from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.network import Route53, ELB, CloudFront ,APIGateway
from diagrams.aws.security import WAF, Cognito
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch
from diagrams.aws.integration import SNS
from diagrams.aws.engagement import SES

with Diagram("AWS E-commerce Site Architecture", show=False, direction="TB"):
    with Cluster("User Interface"):
        s3 = S3("Host static content")
        cloudFront = CloudFront("Deliver content globally")

    with Cluster("Application Layer"):
        lambda_api = Lambda("Serverless Backend")
        apiGateway = APIGateway("API Gateway")
        ec2 = EC2("Application Server")

        lambda_api >> apiGateway
        ec2 >> apiGateway

    with Cluster("Data Layer"):
        rds = RDS("Relational Data")
        dynamodb = Dynamodb("NoSQL Data")

    with Cluster("Authentication & Authorization"):
        cognito = Cognito("User Management")

    with Cluster("Networking"):
        route53 = Route53("DNS")
        elb = ELB("Load Balancer")

    with Cluster("Security & Monitoring"):
        waf = WAF("Web Application Firewall")
        cloudwatch = Cloudwatch("Monitoring")

    with Cluster("Communication & Notification"):
        sns = SNS("Notifications")
        ses = SES("Email Service")

    with Cluster("Storage & CDN"):
        s3_storage = S3("Store & Deliver Content")
        cloudFront_cdn = CloudFront("CDN")

    # Connections
    s3 >> cloudFront >> elb >> ec2
    s3_storage >> cloudFront_cdn
    lambda_api >> dynamodb
    ec2 >> rds
    route53 >> elb
    apiGateway >> lambda_api
    cognito >> apiGateway
    sns >> ses
    ec2 >> cloudwatch
    lambda_api >> cloudwatch
    waf >> elb

# Note: When running this script, make sure you have Graphviz installed as diagrams relies on it to render the diagram.
