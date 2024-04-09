from unittest import result

from sympy import python
# from backend.app.define_function import generate_aws_service_description
# from backend.app.define_function import generate_security_precautions
from define_function import generate_python_code
from create_image import create_agent

# input_text = "Simple Web Application"

# # 関数の呼び出しと返り値の分割
# description, json_result = generate_aws_service_description(input_text)

# print("AWS Service Description:")
# print(description)
# print("\nJSON Result:")
# print(json_result)

# input_text = "S3"

# result = generate_security_precautions(input_text)
# print(result)

input_text = """[
    {
        "name": "Amazon EC2",
        "description": "EC2 instances can host your web application and database servers. You can scale your instances based on traffic demand, ensuring optimal performance.",
        "dependencies": [
            {
                "name": "Amazon RDS",
                "description": "RDS can host your e-commerce database, providing high availability and automatic backups. It integrates seamlessly with EC2 instances, allowing for efficient data access.",
                "type": "database"
            }
        ]
    },
    {
        "name": "Amazon RDS",
        "description": "RDS can host your e-commerce database, providing high availability and automatic backups. It integrates seamlessly with EC2 instances, allowing for efficient data access.",
        "dependencies": []
    },
    {
        "name": "Amazon S3",
        "description": "S3 can store product images, media files, and other static content for your E-commerce site. It can be easily integrated with your web application for fast content delivery.",
        "dependencies": []
    },
    {
        "name": "Amazon CloudFront",
        "description": "CloudFront is a content delivery network that accelerates the delivery of your website content to users worldwide. It can be used in conjunction with S3 to ensure fast and reliable access to your E-commerce site.",
        "dependencies": [
            {
                "name": "Amazon S3",
                "description": "S3 can store product images, media files, and other static content for your E-commerce site. It can be easily integrated with your web application for fast content delivery.",
                "type": "storage"
            }
        ]
    },
    {
        "name": "Amazon Route 53",
        "description": "Route 53 is a scalable DNS service that can route users to the closest AWS edge location for optimal performance. It can be used to manage domain names, ensuring reliable access to your E-commerce site.",
        "dependencies": []
    }
]"""

python_code = generate_python_code(input_text)
print(python_code)
result = create_agent(python_code)
print(result)
