from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.network import Route53, ELB, CloudFront ,APIGateway
from diagrams.aws.security import WAF, CertificateManager, ACM
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch
from diagrams.aws.integration import SNS
from diagrams.aws.engagement import SES


with Diagram("AWS Static Web Hosting Architecture", show=False):
    with Cluster("Static Hosting"):
        s3 = S3("S3 Bucket\nStatic Content")
        cloudFront = CloudFront("CloudFront\nCDN")
        route53 = Route53("Route 53\nDNS")
        acm = CertificateManager("ACM\nSSL/TLS Certificate")
        waf = WAF("WAF\nWeb Application Firewall")

        s3 >> cloudFront >> route53
        cloudFront >> acm
        cloudFront >> waf

    with Cluster("Dynamic Processing (Optional)"):
        lambda_function = Lambda("Lambda\nServer-Side Processing")
        apiGateway = APIGateway("API Gateway")
        cloudFront >> apiGateway >> lambda_function

# Save the diagram to a file
diagram_path = "AWS_Static_Web_Hosting_Architecture"
Diagram.render(diagram_path)

print(f"Diagram saved to {diagram_path}.png")
