
# AWS Services for Building a Static Web Page

When building a static web page on AWS, several services can be utilized to host, manage, and deliver content efficiently and securely. Below are the recommended AWS services:

## 1. Amazon S3 (Simple Storage Service)
- **Primary Use:** Hosting static website content (HTML, CSS, JS, images, videos).
- **Key Features:**
  - Serves static content directly to browsers.
  - High durability, availability, and scalability.
  - Supports custom domain names for website hosting.
- **Considerations:**
  - Manage public access through bucket policies.
  - Integrate with AWS Lambda for dynamic processing if necessary.

## 2. Amazon CloudFront
- **Primary Use:** Distributing static content globally.
- **Key Features:**
  - CDN that caches content at edge locations worldwide.
  - Integrates with S3 and supports SSL/TLS.
  - Advanced caching features for optimized delivery.
- **Considerations:**
  - Optimize cache behavior and utilize AWS Certificate Manager for SSL/TLS certificates.

## 3. Amazon Route 53
- **Primary Use:** Managing DNS and routing for your static website.
- **Key Features:**
  - Highly available DNS web service.
  - Supports domain registration and DNS record management.
- **Considerations:**
  - Configure DNS to point to CloudFront or S3 website endpoint.

## 4. AWS Certificate Manager (ACM)
- **Primary Use:** Managing SSL/TLS certificates.
- **Key Features:**
  - Free public SSL/TLS certificates for AWS resources.
  - Automatic certificate renewal.
- **Considerations:**
  - Use for secure HTTPS connections on CloudFront.

## 5. AWS Lambda (Optional)
- **Primary Use:** Running backend code for dynamic behavior.
- **Key Features:**
  - Serverless execution of code in response to events.
  - Can work with Amazon API Gateway for backend logic.
- **Considerations:**
  - Adds dynamic capabilities to static sites.

## Additional Considerations:
- Implement AWS WAF and Amazon CloudWatch with CloudFront for security and monitoring.
- Optimize content delivery using CloudFront's features.

These services provide a comprehensive platform for hosting, managing, and delivering static web content on AWS, ensuring high performance, reliability, and security.
