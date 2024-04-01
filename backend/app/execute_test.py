from create_image import create_agent

input = """
from diagrams import Diagram
from diagrams.aws.compute import EC2, Lambda, ElasticBeanstalk
from diagrams.aws.database import RDS, DynamoDB
from diagrams.aws.network import ELB, APIGateway, CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.security import IAM

with Diagram("Simple Web Application on AWS", show=False):
    user = ELB("Load Balancer")
    web_app = ElasticBeanstalk("Web App Deployment")
    static_content = S3("Static Content Hosting")
    backend_api = Lambda("Serverless Backend")
    db = RDS("Relational DB")
    no_sql_db = DynamoDB("NoSQL DB")
    api_gw = APIGateway("API Gateway")
    cloud_front = CloudFront("CDN")
    compute_ec2 = EC2("Backend Compute")
    iam = IAM("Access Management")

    user >> web_app >> static_content
    user >> api_gw >> backend_api
    backend_api >> db
    backend_api >> no_sql_db
    static_content >> cloud_front
    web_app >> compute_ec2
    user >> iam"""
result = create_agent(input)
print(result)

