from itertools import chain
import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

def generate_aws_service_description(input_text):
    """
    Generate a description of AWS services based on the input text.

    Args:
        input_text (str): Input text to generate the AWS service description.

    Returns:
        tuple: A tuple containing the description of AWS services in markdown format
               and the result of json_chain.
    """
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=1.0, max_tokens=1000)
    description_output_parser = StrOutputParser()
    description_prompt = ChatPromptTemplate.from_template("""Must return markdown format.\nPlease tell me more about the AWS services you should use when building {input}.\n""")
    description_chain = description_prompt | model | description_output_parser
    description = description_chain.invoke({"input": input_text})

    json_output_parser = JsonOutputParser()
    json_prompt = ChatPromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["description"],
        partial_variables={"format_instructions": json_output_parser.get_format_instructions()}
    )
    json_chain = json_prompt | model | json_output_parser
    json_result = json_chain.invoke({"description": description})

    return description, json_result

def generate_python_code(input_text):
    """
    Generate Python code based on the input text.

    Args:
        input_text (str): Input text to generate the Python code.

    Returns:
        str: Python code.
    """
    model = ChatOpenAI(model="gpt-4-0125-preview", temperature=1.0, max_tokens=1000)
    output_parser = StrOutputParser()
    prompt = ChatPromptTemplate.from_template("""Express what you receive with {input} in python diagrams. There is no need to run it. Please do not return anything other than python code.""")
    chain = ({"input": input_text} | prompt | model | output_parser)
    return chain.invoke({"input": "Simple Web Application"})

def generate_security_precautions(input_text, service_description):
    """
    Generate a description of security precautions based on the input text and AWS service description.

    Args:
        input_text (str): Input text to generate the security precautions.
        service_description (str): Description of AWS services.

    Returns:
        str: Description of security precautions in markdown format.
    """
    model = ChatOpenAI(model="gpt-4-0125-preview", temperature=1.0, max_tokens=1000)
    output_parser = StrOutputParser()
    prompt = ChatPromptTemplate.from_template("""Must return markdown format.\n Please tell me what security precautions I need to take when using the services below.\n {input} """)
    chain = ({"input": service_description} | prompt | model | output_parser)
    return chain.invoke({"input": input_text})




# うまくいかなかったら以下を参照させると良いかもしれない

# The following modules are available.
#     aws.analytics
#     Analyticsdiagrams.aws.analytics.Analytics

#     Athenadiagrams.aws.analytics.Athena

#     CloudsearchSearchDocumentsdiagrams.aws.analytics.CloudsearchSearchDocuments

#     Cloudsearchdiagrams.aws.analytics.Cloudsearch

#     DataLakeResourcediagrams.aws.analytics.DataLakeResource

#     DataPipelinediagrams.aws.analytics.DataPipeline

#     ElasticsearchServicediagrams.aws.analytics.ElasticsearchService, ES (alias)

#     EMRClusterdiagrams.aws.analytics.EMRCluster

#     EMREngineMaprM3diagrams.aws.analytics.EMREngineMaprM3

#     EMREngineMaprM5diagrams.aws.analytics.EMREngineMaprM5

#     EMREngineMaprM7diagrams.aws.analytics.EMREngineMaprM7

#     EMREnginediagrams.aws.analytics.EMREngine

#     EMRHdfsClusterdiagrams.aws.analytics.EMRHdfsCluster

#     EMRdiagrams.aws.analytics.EMR

#     GlueCrawlersdiagrams.aws.analytics.GlueCrawlers

#     GlueDataCatalogdiagrams.aws.analytics.GlueDataCatalog

#     Gluediagrams.aws.analytics.Glue

#     KinesisDataAnalyticsdiagrams.aws.analytics.KinesisDataAnalytics

#     KinesisDataFirehosediagrams.aws.analytics.KinesisDataFirehose

#     KinesisDataStreamsdiagrams.aws.analytics.KinesisDataStreams

#     KinesisVideoStreamsdiagrams.aws.analytics.KinesisVideoStreams

#     Kinesisdiagrams.aws.analytics.Kinesis

#     LakeFormationdiagrams.aws.analytics.LakeFormation

#     ManagedStreamingForKafkadiagrams.aws.analytics.ManagedStreamingForKafka

#     Quicksightdiagrams.aws.analytics.Quicksight

#     RedshiftDenseComputeNodediagrams.aws.analytics.RedshiftDenseComputeNode

#     RedshiftDenseStorageNodediagrams.aws.analytics.RedshiftDenseStorageNode

#     Redshiftdiagrams.aws.analytics.Redshift

#     aws.ar
#     ArVrdiagrams.aws.ar.ArVr

#     Sumeriandiagrams.aws.ar.Sumerian

#     aws.blockchain
#     BlockchainResourcediagrams.aws.blockchain.BlockchainResource

#     Blockchaindiagrams.aws.blockchain.Blockchain

#     ManagedBlockchaindiagrams.aws.blockchain.ManagedBlockchain

#     QuantumLedgerDatabaseQldbdiagrams.aws.blockchain.QuantumLedgerDatabaseQldb, QLDB (alias)

#     aws.business
#     AlexaForBusinessdiagrams.aws.business.AlexaForBusiness, A4B (alias)

#     BusinessApplicationsdiagrams.aws.business.BusinessApplications

#     Chimediagrams.aws.business.Chime

#     Workmaildiagrams.aws.business.Workmail

#     aws.compute
#     AppRunnerdiagrams.aws.compute.AppRunner

#     ApplicationAutoScalingdiagrams.aws.compute.ApplicationAutoScaling, AutoScaling (alias)

#     Batchdiagrams.aws.compute.Batch

#     ComputeOptimizerdiagrams.aws.compute.ComputeOptimizer

#     Computediagrams.aws.compute.Compute

#     EC2Amidiagrams.aws.compute.EC2Ami, AMI (alias)

#     EC2AutoScalingdiagrams.aws.compute.EC2AutoScaling

#     EC2ContainerRegistryImagediagrams.aws.compute.EC2ContainerRegistryImage

#     EC2ContainerRegistryRegistrydiagrams.aws.compute.EC2ContainerRegistryRegistry

#     EC2ContainerRegistrydiagrams.aws.compute.EC2ContainerRegistry, ECR (alias)

#     EC2ElasticIpAddressdiagrams.aws.compute.EC2ElasticIpAddress

#     EC2ImageBuilderdiagrams.aws.compute.EC2ImageBuilder

#     EC2Instancediagrams.aws.compute.EC2Instance

#     EC2Instancesdiagrams.aws.compute.EC2Instances

#     EC2Rescuediagrams.aws.compute.EC2Rescue

#     EC2SpotInstancediagrams.aws.compute.EC2SpotInstance

#     EC2diagrams.aws.compute.EC2

#     ElasticBeanstalkApplicationdiagrams.aws.compute.ElasticBeanstalkApplication

#     ElasticBeanstalkDeploymentdiagrams.aws.compute.ElasticBeanstalkDeployment

#     ElasticBeanstalkdiagrams.aws.compute.ElasticBeanstalk, EB (alias)

#     ElasticContainerServiceContainerdiagrams.aws.compute.ElasticContainerServiceContainer

#     ElasticContainerServiceServicediagrams.aws.compute.ElasticContainerServiceService

#     ElasticContainerServicediagrams.aws.compute.ElasticContainerService, ECS (alias)

#     ElasticKubernetesServicediagrams.aws.compute.ElasticKubernetesService, EKS (alias)

#     Fargatediagrams.aws.compute.Fargate

#     LambdaFunctiondiagrams.aws.compute.LambdaFunction

#     Lambdadiagrams.aws.compute.Lambda

#     Lightsaildiagrams.aws.compute.Lightsail

#     LocalZonesdiagrams.aws.compute.LocalZones

#     Outpostsdiagrams.aws.compute.Outposts

#     ServerlessApplicationRepositorydiagrams.aws.compute.ServerlessApplicationRepository, SAR (alias)

#     ThinkboxDeadlinediagrams.aws.compute.ThinkboxDeadline

#     ThinkboxDraftdiagrams.aws.compute.ThinkboxDraft

#     ThinkboxFrostdiagrams.aws.compute.ThinkboxFrost

#     ThinkboxKrakatoadiagrams.aws.compute.ThinkboxKrakatoa

#     ThinkboxSequoiadiagrams.aws.compute.ThinkboxSequoia

#     ThinkboxStokediagrams.aws.compute.ThinkboxStoke

#     ThinkboxXmeshdiagrams.aws.compute.ThinkboxXmesh

#     VmwareCloudOnAWSdiagrams.aws.compute.VmwareCloudOnAWS

#     Wavelengthdiagrams.aws.compute.Wavelength

#     aws.cost
#     Budgetsdiagrams.aws.cost.Budgets

#     CostAndUsageReportdiagrams.aws.cost.CostAndUsageReport

#     CostExplorerdiagrams.aws.cost.CostExplorer

#     CostManagementdiagrams.aws.cost.CostManagement

#     ReservedInstanceReportingdiagrams.aws.cost.ReservedInstanceReporting

#     SavingsPlansdiagrams.aws.cost.SavingsPlans

#     aws.database
#     AuroraInstancediagrams.aws.database.AuroraInstance

#     Auroradiagrams.aws.database.Aurora

#     DatabaseMigrationServiceDatabaseMigrationWorkflowdiagrams.aws.database.DatabaseMigrationServiceDatabaseMigrationWorkflow

#     DatabaseMigrationServicediagrams.aws.database.DatabaseMigrationService, DMS (alias)

#     Databasediagrams.aws.database.Database, DB (alias)

#     DocumentdbMongodbCompatibilitydiagrams.aws.database.DocumentdbMongodbCompatibility, DocumentDB (alias)

#     DynamodbAttributediagrams.aws.database.DynamodbAttribute

#     DynamodbAttributesdiagrams.aws.database.DynamodbAttributes

#     DynamodbDaxdiagrams.aws.database.DynamodbDax, DAX (alias)

#     DynamodbGlobalSecondaryIndexdiagrams.aws.database.DynamodbGlobalSecondaryIndex, DynamodbGSI (alias)

#     DynamodbItemdiagrams.aws.database.DynamodbItem

#     DynamodbItemsdiagrams.aws.database.DynamodbItems

#     DynamodbTablediagrams.aws.database.DynamodbTable

#     Dynamodbdiagrams.aws.database.Dynamodb, DDB (alias)

#     ElasticacheCacheNodediagrams.aws.database.ElasticacheCacheNode

#     ElasticacheForMemcacheddiagrams.aws.database.ElasticacheForMemcached

#     ElasticacheForRedisdiagrams.aws.database.ElasticacheForRedis

#     Elasticachediagrams.aws.database.Elasticache, ElastiCache (alias)

#     KeyspacesManagedApacheCassandraServicediagrams.aws.database.KeyspacesManagedApacheCassandraService

#     Neptunediagrams.aws.database.Neptune

#     QuantumLedgerDatabaseQldbdiagrams.aws.database.QuantumLedgerDatabaseQldb, QLDB (alias)

#     RDSInstancediagrams.aws.database.RDSInstance

#     RDSMariadbInstancediagrams.aws.database.RDSMariadbInstance

#     RDSMysqlInstancediagrams.aws.database.RDSMysqlInstance

#     RDSOnVmwarediagrams.aws.database.RDSOnVmware

#     RDSOracleInstancediagrams.aws.database.RDSOracleInstance

#     RDSPostgresqlInstancediagrams.aws.database.RDSPostgresqlInstance

#     RDSSqlServerInstancediagrams.aws.database.RDSSqlServerInstance

#     RDSdiagrams.aws.database.RDS

#     RedshiftDenseComputeNodediagrams.aws.database.RedshiftDenseComputeNode

#     RedshiftDenseStorageNodediagrams.aws.database.RedshiftDenseStorageNode

#     Redshiftdiagrams.aws.database.Redshift

#     Timestreamdiagrams.aws.database.Timestream

#     aws.devtools
#     CloudDevelopmentKitdiagrams.aws.devtools.CloudDevelopmentKit

#     Cloud9Resourcediagrams.aws.devtools.Cloud9Resource

#     Cloud9diagrams.aws.devtools.Cloud9

#     Codebuilddiagrams.aws.devtools.Codebuild

#     Codecommitdiagrams.aws.devtools.Codecommit

#     Codedeploydiagrams.aws.devtools.Codedeploy

#     Codepipelinediagrams.aws.devtools.Codepipeline

#     Codestardiagrams.aws.devtools.Codestar

#     CommandLineInterfacediagrams.aws.devtools.CommandLineInterface, CLI (alias)

#     DeveloperToolsdiagrams.aws.devtools.DeveloperTools, DevTools (alias)

#     ToolsAndSdksdiagrams.aws.devtools.ToolsAndSdks

#     XRaydiagrams.aws.devtools.XRay

#     aws.enablement
#     CustomerEnablementdiagrams.aws.enablement.CustomerEnablement

#     Iqdiagrams.aws.enablement.Iq

#     ManagedServicesdiagrams.aws.enablement.ManagedServices

#     ProfessionalServicesdiagrams.aws.enablement.ProfessionalServices

#     Supportdiagrams.aws.enablement.Support

#     aws.enduser
#     Appstream20diagrams.aws.enduser.Appstream20

#     DesktopAndAppStreamingdiagrams.aws.enduser.DesktopAndAppStreaming

#     Workdocsdiagrams.aws.enduser.Workdocs

#     Worklinkdiagrams.aws.enduser.Worklink

#     Workspacesdiagrams.aws.enduser.Workspaces

#     aws.engagement
#     Connectdiagrams.aws.engagement.Connect

#     CustomerEngagementdiagrams.aws.engagement.CustomerEngagement

#     Pinpointdiagrams.aws.engagement.Pinpoint

#     SimpleEmailServiceSesEmaildiagrams.aws.engagement.SimpleEmailServiceSesEmail

#     SimpleEmailServiceSesdiagrams.aws.engagement.SimpleEmailServiceSes, SES (alias)

#     aws.game
#     GameTechdiagrams.aws.game.GameTech

#     Gameliftdiagrams.aws.game.Gamelift

#     aws.general
#     Clientdiagrams.aws.general.Client

#     Diskdiagrams.aws.general.Disk

#     Forumsdiagrams.aws.general.Forums

#     Generaldiagrams.aws.general.General

#     GenericDatabasediagrams.aws.general.GenericDatabase

#     GenericFirewalldiagrams.aws.general.GenericFirewall

#     GenericOfficeBuildingdiagrams.aws.general.GenericOfficeBuilding, OfficeBuilding (alias)

#     GenericSamlTokendiagrams.aws.general.GenericSamlToken

#     GenericSDKdiagrams.aws.general.GenericSDK

#     InternetAlt1diagrams.aws.general.InternetAlt1

#     InternetAlt2diagrams.aws.general.InternetAlt2

#     InternetGatewaydiagrams.aws.general.InternetGateway

#     Marketplacediagrams.aws.general.Marketplace

#     MobileClientdiagrams.aws.general.MobileClient

#     Multimediadiagrams.aws.general.Multimedia

#     OfficeBuildingdiagrams.aws.general.OfficeBuilding

#     SamlTokendiagrams.aws.general.SamlToken

#     SDKdiagrams.aws.general.SDK

#     SslPadlockdiagrams.aws.general.SslPadlock

#     TapeStoragediagrams.aws.general.TapeStorage

#     Toolkitdiagrams.aws.general.Toolkit

#     TraditionalServerdiagrams.aws.general.TraditionalServer

#     Userdiagrams.aws.general.User

#     Usersdiagrams.aws.general.Users

#     aws.integration
#     ApplicationIntegrationdiagrams.aws.integration.ApplicationIntegration

#     Appsyncdiagrams.aws.integration.Appsync

#     ConsoleMobileApplicationdiagrams.aws.integration.ConsoleMobileApplication

#     EventResourcediagrams.aws.integration.EventResource

#     EventbridgeCustomEventBusResourcediagrams.aws.integration.EventbridgeCustomEventBusResource

#     EventbridgeDefaultEventBusResourcediagrams.aws.integration.EventbridgeDefaultEventBusResource

#     EventbridgeSaasPartnerEventBusResourcediagrams.aws.integration.EventbridgeSaasPartnerEventBusResource

#     Eventbridgediagrams.aws.integration.Eventbridge

#     ExpressWorkflowsdiagrams.aws.integration.ExpressWorkflows

#     MQdiagrams.aws.integration.MQ

#     SimpleNotificationServiceSnsEmailNotificationdiagrams.aws.integration.SimpleNotificationServiceSnsEmailNotification

#     SimpleNotificationServiceSnsHttpNotificationdiagrams.aws.integration.SimpleNotificationServiceSnsHttpNotification

#     SimpleNotificationServiceSnsTopicdiagrams.aws.integration.SimpleNotificationServiceSnsTopic

#     SimpleNotificationServiceSnsdiagrams.aws.integration.SimpleNotificationServiceSns, SNS (alias)

#     SimpleQueueServiceSqsMessagediagrams.aws.integration.SimpleQueueServiceSqsMessage

#     SimpleQueueServiceSqsQueuediagrams.aws.integration.SimpleQueueServiceSqsQueue

#     SimpleQueueServiceSqsdiagrams.aws.integration.SimpleQueueServiceSqs, SQS (alias)

#     StepFunctionsdiagrams.aws.integration.StepFunctions, SF (alias)

#     aws.iot
#     Freertosdiagrams.aws.iot.Freertos, FreeRTOS (alias)

#     InternetOfThingsdiagrams.aws.iot.InternetOfThings

#     Iot1Clickdiagrams.aws.iot.Iot1Click

#     IotActiondiagrams.aws.iot.IotAction

#     IotActuatordiagrams.aws.iot.IotActuator

#     IotAlexaEchodiagrams.aws.iot.IotAlexaEcho

#     IotAlexaEnabledDevicediagrams.aws.iot.IotAlexaEnabledDevice

#     IotAlexaSkilldiagrams.aws.iot.IotAlexaSkill

#     IotAlexaVoiceServicediagrams.aws.iot.IotAlexaVoiceService

#     IotAnalyticsChanneldiagrams.aws.iot.IotAnalyticsChannel

#     IotAnalyticsDataSetdiagrams.aws.iot.IotAnalyticsDataSet

#     IotAnalyticsDataStorediagrams.aws.iot.IotAnalyticsDataStore

#     IotAnalyticsNotebookdiagrams.aws.iot.IotAnalyticsNotebook

#     IotAnalyticsPipelinediagrams.aws.iot.IotAnalyticsPipeline

#     IotAnalyticsdiagrams.aws.iot.IotAnalytics

#     IotBankdiagrams.aws.iot.IotBank

#     IotBicyclediagrams.aws.iot.IotBicycle

#     IotButtondiagrams.aws.iot.IotButton

#     IotCameradiagrams.aws.iot.IotCamera

#     IotCardiagrams.aws.iot.IotCar

#     IotCartdiagrams.aws.iot.IotCart

#     IotCertificatediagrams.aws.iot.IotCertificate

#     IotCoffeePotdiagrams.aws.iot.IotCoffeePot

#     IotCorediagrams.aws.iot.IotCore

#     IotDesiredStatediagrams.aws.iot.IotDesiredState

#     IotDeviceDefenderdiagrams.aws.iot.IotDeviceDefender

#     IotDeviceGatewaydiagrams.aws.iot.IotDeviceGateway

#     IotDeviceManagementdiagrams.aws.iot.IotDeviceManagement

#     IotDoorLockdiagrams.aws.iot.IotDoorLock

#     IotEventsdiagrams.aws.iot.IotEvents

#     IotFactorydiagrams.aws.iot.IotFactory

#     IotFireTvStickdiagrams.aws.iot.IotFireTvStick

#     IotFireTvdiagrams.aws.iot.IotFireTv

#     IotGenericdiagrams.aws.iot.IotGeneric

#     IotGreengrassConnectordiagrams.aws.iot.IotGreengrassConnector

#     IotGreengrassdiagrams.aws.iot.IotGreengrass

#     IotHardwareBoarddiagrams.aws.iot.IotHardwareBoard, IotBoard (alias)

#     IotHousediagrams.aws.iot.IotHouse

#     IotHttpdiagrams.aws.iot.IotHttp

#     IotHttp2diagrams.aws.iot.IotHttp2

#     IotJobsdiagrams.aws.iot.IotJobs

#     IotLambdadiagrams.aws.iot.IotLambda

#     IotLightbulbdiagrams.aws.iot.IotLightbulb

#     IotMedicalEmergencydiagrams.aws.iot.IotMedicalEmergency

#     IotMqttdiagrams.aws.iot.IotMqtt

#     IotOverTheAirUpdatediagrams.aws.iot.IotOverTheAirUpdate

#     IotPolicyEmergencydiagrams.aws.iot.IotPolicyEmergency

#     IotPolicydiagrams.aws.iot.IotPolicy

#     IotReportedStatediagrams.aws.iot.IotReportedState

#     IotRulediagrams.aws.iot.IotRule

#     IotSensordiagrams.aws.iot.IotSensor

#     IotServodiagrams.aws.iot.IotServo

#     IotShadowdiagrams.aws.iot.IotShadow

#     IotSimulatordiagrams.aws.iot.IotSimulator

#     IotSitewisediagrams.aws.iot.IotSitewise

#     IotThermostatdiagrams.aws.iot.IotThermostat

#     IotThingsGraphdiagrams.aws.iot.IotThingsGraph

#     IotTopicdiagrams.aws.iot.IotTopic

#     IotTraveldiagrams.aws.iot.IotTravel

#     IotUtilitydiagrams.aws.iot.IotUtility

#     IotWindfarmdiagrams.aws.iot.IotWindfarm

#     aws.management
#     AutoScalingdiagrams.aws.management.AutoScaling

#     Chatbotdiagrams.aws.management.Chatbot

#     CloudformationChangeSetdiagrams.aws.management.CloudformationChangeSet

#     CloudformationStackdiagrams.aws.management.CloudformationStack

#     CloudformationTemplatediagrams.aws.management.CloudformationTemplate

#     Cloudformationdiagrams.aws.management.Cloudformation

#     Cloudtraildiagrams.aws.management.Cloudtrail

#     CloudwatchAlarmdiagrams.aws.management.CloudwatchAlarm

#     CloudwatchEventEventBaseddiagrams.aws.management.CloudwatchEventEventBased

#     CloudwatchEventTimeBaseddiagrams.aws.management.CloudwatchEventTimeBased

#     CloudwatchRulediagrams.aws.management.CloudwatchRule

#     Cloudwatchdiagrams.aws.management.Cloudwatch

#     Codegurudiagrams.aws.management.Codeguru

#     CommandLineInterfacediagrams.aws.management.CommandLineInterface

#     Configdiagrams.aws.management.Config

#     ControlTowerdiagrams.aws.management.ControlTower

#     LicenseManagerdiagrams.aws.management.LicenseManager

#     ManagedServicesdiagrams.aws.management.ManagedServices

#     ManagementAndGovernancediagrams.aws.management.ManagementAndGovernance

#     ManagementConsolediagrams.aws.management.ManagementConsole

#     OpsworksAppsdiagrams.aws.management.OpsworksApps

#     OpsworksDeploymentsdiagrams.aws.management.OpsworksDeployments

#     OpsworksInstancesdiagrams.aws.management.OpsworksInstances

#     OpsworksLayersdiagrams.aws.management.OpsworksLayers

#     OpsworksMonitoringdiagrams.aws.management.OpsworksMonitoring

#     OpsworksPermissionsdiagrams.aws.management.OpsworksPermissions

#     OpsworksResourcesdiagrams.aws.management.OpsworksResources

#     OpsworksStackdiagrams.aws.management.OpsworksStack

#     Opsworksdiagrams.aws.management.Opsworks

#     OrganizationsAccountdiagrams.aws.management.OrganizationsAccount

#     OrganizationsOrganizationalUnitdiagrams.aws.management.OrganizationsOrganizationalUnit

#     Organizationsdiagrams.aws.management.Organizations

#     PersonalHealthDashboarddiagrams.aws.management.PersonalHealthDashboard

#     ServiceCatalogdiagrams.aws.management.ServiceCatalog

#     SystemsManagerAutomationdiagrams.aws.management.SystemsManagerAutomation

#     SystemsManagerDocumentsdiagrams.aws.management.SystemsManagerDocuments

#     SystemsManagerInventorydiagrams.aws.management.SystemsManagerInventory

#     SystemsManagerMaintenanceWindowsdiagrams.aws.management.SystemsManagerMaintenanceWindows

#     SystemsManagerOpscenterdiagrams.aws.management.SystemsManagerOpscenter

#     SystemsManagerParameterStorediagrams.aws.management.SystemsManagerParameterStore, ParameterStore (alias)

#     SystemsManagerPatchManagerdiagrams.aws.management.SystemsManagerPatchManager

#     SystemsManagerRunCommanddiagrams.aws.management.SystemsManagerRunCommand

#     SystemsManagerStateManagerdiagrams.aws.management.SystemsManagerStateManager

#     SystemsManagerdiagrams.aws.management.SystemsManager, SSM (alias)

#     TrustedAdvisorChecklistCostdiagrams.aws.management.TrustedAdvisorChecklistCost

#     TrustedAdvisorChecklistFaultTolerantdiagrams.aws.management.TrustedAdvisorChecklistFaultTolerant

#     TrustedAdvisorChecklistPerformancediagrams.aws.management.TrustedAdvisorChecklistPerformance

#     TrustedAdvisorChecklistSecuritydiagrams.aws.management.TrustedAdvisorChecklistSecurity

#     TrustedAdvisorChecklistdiagrams.aws.management.TrustedAdvisorChecklist

#     TrustedAdvisordiagrams.aws.management.TrustedAdvisor

#     WellArchitectedTooldiagrams.aws.management.WellArchitectedTool

#     aws.media
#     ElasticTranscoderdiagrams.aws.media.ElasticTranscoder

#     ElementalConductordiagrams.aws.media.ElementalConductor

#     ElementalDeltadiagrams.aws.media.ElementalDelta

#     ElementalLivediagrams.aws.media.ElementalLive

#     ElementalMediaconnectdiagrams.aws.media.ElementalMediaconnect

#     ElementalMediaconvertdiagrams.aws.media.ElementalMediaconvert

#     ElementalMedialivediagrams.aws.media.ElementalMedialive

#     ElementalMediapackagediagrams.aws.media.ElementalMediapackage

#     ElementalMediastorediagrams.aws.media.ElementalMediastore

#     ElementalMediatailordiagrams.aws.media.ElementalMediatailor

#     ElementalServerdiagrams.aws.media.ElementalServer

#     KinesisVideoStreamsdiagrams.aws.media.KinesisVideoStreams

#     MediaServicesdiagrams.aws.media.MediaServices

#     aws.migration
#     ApplicationDiscoveryServicediagrams.aws.migration.ApplicationDiscoveryService, ADS (alias)

#     CloudendureMigrationdiagrams.aws.migration.CloudendureMigration, CEM (alias)

#     DatabaseMigrationServicediagrams.aws.migration.DatabaseMigrationService, DMS (alias)

#     DatasyncAgentdiagrams.aws.migration.DatasyncAgent

#     Datasyncdiagrams.aws.migration.Datasync

#     MigrationAndTransferdiagrams.aws.migration.MigrationAndTransfer, MAT (alias)

#     MigrationHubdiagrams.aws.migration.MigrationHub

#     ServerMigrationServicediagrams.aws.migration.ServerMigrationService, SMS (alias)

#     SnowballEdgediagrams.aws.migration.SnowballEdge

#     Snowballdiagrams.aws.migration.Snowball

#     Snowmobilediagrams.aws.migration.Snowmobile

#     TransferForSftpdiagrams.aws.migration.TransferForSftp

#     aws.ml
#     ApacheMxnetOnAWSdiagrams.aws.ml.ApacheMxnetOnAWS

#     AugmentedAidiagrams.aws.ml.AugmentedAi

#     Comprehenddiagrams.aws.ml.Comprehend

#     DeepLearningAmisdiagrams.aws.ml.DeepLearningAmis

#     DeepLearningContainersdiagrams.aws.ml.DeepLearningContainers, DLC (alias)

#     Deepcomposerdiagrams.aws.ml.Deepcomposer

#     Deeplensdiagrams.aws.ml.Deeplens

#     Deepracerdiagrams.aws.ml.Deepracer

#     ElasticInferencediagrams.aws.ml.ElasticInference

#     Forecastdiagrams.aws.ml.Forecast

#     FraudDetectordiagrams.aws.ml.FraudDetector

#     Kendradiagrams.aws.ml.Kendra

#     Lexdiagrams.aws.ml.Lex

#     MachineLearningdiagrams.aws.ml.MachineLearning

#     Personalizediagrams.aws.ml.Personalize

#     Pollydiagrams.aws.ml.Polly

#     RekognitionImagediagrams.aws.ml.RekognitionImage

#     RekognitionVideodiagrams.aws.ml.RekognitionVideo

#     Rekognitiondiagrams.aws.ml.Rekognition

#     SagemakerGroundTruthdiagrams.aws.ml.SagemakerGroundTruth

#     SagemakerModeldiagrams.aws.ml.SagemakerModel

#     SagemakerNotebookdiagrams.aws.ml.SagemakerNotebook

#     SagemakerTrainingJobdiagrams.aws.ml.SagemakerTrainingJob

#     Sagemakerdiagrams.aws.ml.Sagemaker

#     TensorflowOnAWSdiagrams.aws.ml.TensorflowOnAWS

#     Textractdiagrams.aws.ml.Textract

#     Transcribediagrams.aws.ml.Transcribe

#     Translatediagrams.aws.ml.Translate

#     aws.mobile
#     Amplifydiagrams.aws.mobile.Amplify

#     APIGatewayEndpointdiagrams.aws.mobile.APIGatewayEndpoint

#     APIGatewaydiagrams.aws.mobile.APIGateway

#     Appsyncdiagrams.aws.mobile.Appsync

#     DeviceFarmdiagrams.aws.mobile.DeviceFarm

#     Mobilediagrams.aws.mobile.Mobile

#     Pinpointdiagrams.aws.mobile.Pinpoint

#     aws.network
#     APIGatewayEndpointdiagrams.aws.network.APIGatewayEndpoint

#     APIGatewaydiagrams.aws.network.APIGateway

#     AppMeshdiagrams.aws.network.AppMesh

#     ClientVpndiagrams.aws.network.ClientVpn

#     CloudMapdiagrams.aws.network.CloudMap

#     CloudFrontDownloadDistributiondiagrams.aws.network.CloudFrontDownloadDistribution

#     CloudFrontEdgeLocationdiagrams.aws.network.CloudFrontEdgeLocation

#     CloudFrontStreamingDistributiondiagrams.aws.network.CloudFrontStreamingDistribution

#     CloudFrontdiagrams.aws.network.CloudFront, CF (alias)

#     DirectConnectdiagrams.aws.network.DirectConnect

#     ElasticLoadBalancingdiagrams.aws.network.ElasticLoadBalancing, ELB (alias)

#     ElbApplicationLoadBalancerdiagrams.aws.network.ElbApplicationLoadBalancer, ALB (alias)

#     ElbClassicLoadBalancerdiagrams.aws.network.ElbClassicLoadBalancer, CLB (alias)

#     ElbNetworkLoadBalancerdiagrams.aws.network.ElbNetworkLoadBalancer, NLB (alias)

#     Endpointdiagrams.aws.network.Endpoint

#     GlobalAcceleratordiagrams.aws.network.GlobalAccelerator, GAX (alias)

#     InternetGatewaydiagrams.aws.network.InternetGateway

#     Nacldiagrams.aws.network.Nacl

#     NATGatewaydiagrams.aws.network.NATGateway

#     NetworkingAndContentDeliverydiagrams.aws.network.NetworkingAndContentDelivery

#     PrivateSubnetdiagrams.aws.network.PrivateSubnet

#     Privatelinkdiagrams.aws.network.Privatelink

#     PublicSubnetdiagrams.aws.network.PublicSubnet

#     Route53HostedZonediagrams.aws.network.Route53HostedZone

#     Route53diagrams.aws.network.Route53

#     RouteTablediagrams.aws.network.RouteTable

#     SiteToSiteVpndiagrams.aws.network.SiteToSiteVpn

#     TransitGatewaydiagrams.aws.network.TransitGateway

#     VPCCustomerGatewaydiagrams.aws.network.VPCCustomerGateway

#     VPCElasticNetworkAdapterdiagrams.aws.network.VPCElasticNetworkAdapter

#     VPCElasticNetworkInterfacediagrams.aws.network.VPCElasticNetworkInterface

#     VPCFlowLogsdiagrams.aws.network.VPCFlowLogs

#     VPCPeeringdiagrams.aws.network.VPCPeering

#     VPCRouterdiagrams.aws.network.VPCRouter

#     VPCTrafficMirroringdiagrams.aws.network.VPCTrafficMirroring

#     VPCdiagrams.aws.network.VPC

#     VpnConnectiondiagrams.aws.network.VpnConnection

#     VpnGatewaydiagrams.aws.network.VpnGateway

#     aws.quantum
#     Braketdiagrams.aws.quantum.Braket

#     QuantumTechnologiesdiagrams.aws.quantum.QuantumTechnologies

#     aws.robotics
#     RobomakerCloudExtensionRosdiagrams.aws.robotics.RobomakerCloudExtensionRos

#     RobomakerDevelopmentEnvironmentdiagrams.aws.robotics.RobomakerDevelopmentEnvironment

#     RobomakerFleetManagementdiagrams.aws.robotics.RobomakerFleetManagement

#     RobomakerSimulatordiagrams.aws.robotics.RobomakerSimulator

#     Robomakerdiagrams.aws.robotics.Robomaker

#     Roboticsdiagrams.aws.robotics.Robotics

#     aws.satellite
#     GroundStationdiagrams.aws.satellite.GroundStation

#     Satellitediagrams.aws.satellite.Satellite

#     aws.security
#     AdConnectordiagrams.aws.security.AdConnector

#     Artifactdiagrams.aws.security.Artifact

#     CertificateAuthoritydiagrams.aws.security.CertificateAuthority

#     CertificateManagerdiagrams.aws.security.CertificateManager, ACM (alias)

#     CloudDirectorydiagrams.aws.security.CloudDirectory

#     Cloudhsmdiagrams.aws.security.Cloudhsm, CloudHSM (alias)

#     Cognitodiagrams.aws.security.Cognito

#     Detectivediagrams.aws.security.Detective

#     DirectoryServicediagrams.aws.security.DirectoryService, DS (alias)

#     FirewallManagerdiagrams.aws.security.FirewallManager, FMS (alias)

#     Guarddutydiagrams.aws.security.Guardduty

#     IdentityAndAccessManagementIamAccessAnalyzerdiagrams.aws.security.IdentityAndAccessManagementIamAccessAnalyzer, IAMAccessAnalyzer (alias)

#     IdentityAndAccessManagementIamAddOndiagrams.aws.security.IdentityAndAccessManagementIamAddOn

#     IdentityAndAccessManagementIamAWSStsAlternatediagrams.aws.security.IdentityAndAccessManagementIamAWSStsAlternate

#     IdentityAndAccessManagementIamAWSStsdiagrams.aws.security.IdentityAndAccessManagementIamAWSSts, IAMAWSSts (alias)

#     IdentityAndAccessManagementIamDataEncryptionKeydiagrams.aws.security.IdentityAndAccessManagementIamDataEncryptionKey

#     IdentityAndAccessManagementIamEncryptedDatadiagrams.aws.security.IdentityAndAccessManagementIamEncryptedData

#     IdentityAndAccessManagementIamLongTermSecurityCredentialdiagrams.aws.security.IdentityAndAccessManagementIamLongTermSecurityCredential

#     IdentityAndAccessManagementIamMfaTokendiagrams.aws.security.IdentityAndAccessManagementIamMfaToken

#     IdentityAndAccessManagementIamPermissionsdiagrams.aws.security.IdentityAndAccessManagementIamPermissions, IAMPermissions (alias)

#     IdentityAndAccessManagementIamRolediagrams.aws.security.IdentityAndAccessManagementIamRole, IAMRole (alias)

#     IdentityAndAccessManagementIamTemporarySecurityCredentialdiagrams.aws.security.IdentityAndAccessManagementIamTemporarySecurityCredential

#     IdentityAndAccessManagementIamdiagrams.aws.security.IdentityAndAccessManagementIam, IAM (alias)

#     InspectorAgentdiagrams.aws.security.InspectorAgent

#     Inspectordiagrams.aws.security.Inspector

#     KeyManagementServicediagrams.aws.security.KeyManagementService, KMS (alias)

#     Maciediagrams.aws.security.Macie

#     ManagedMicrosoftAddiagrams.aws.security.ManagedMicrosoftAd

#     ResourceAccessManagerdiagrams.aws.security.ResourceAccessManager, RAM (alias)

#     SecretsManagerdiagrams.aws.security.SecretsManager

#     SecurityHubFindingdiagrams.aws.security.SecurityHubFinding

#     SecurityHubdiagrams.aws.security.SecurityHub

#     SecurityIdentityAndCompliancediagrams.aws.security.SecurityIdentityAndCompliance

#     ShieldAdvanceddiagrams.aws.security.ShieldAdvanced

#     Shielddiagrams.aws.security.Shield

#     SimpleAddiagrams.aws.security.SimpleAd

#     SingleSignOndiagrams.aws.security.SingleSignOn

#     WAFFilteringRulediagrams.aws.security.WAFFilteringRule

#     WAFdiagrams.aws.security.WAF

#     aws.storage
#     Backupdiagrams.aws.storage.Backup

#     CloudendureDisasterRecoverydiagrams.aws.storage.CloudendureDisasterRecovery, CDR (alias)

#     EFSInfrequentaccessPrimaryBgdiagrams.aws.storage.EFSInfrequentaccessPrimaryBg

#     EFSStandardPrimaryBgdiagrams.aws.storage.EFSStandardPrimaryBg

#     ElasticBlockStoreEBSSnapshotdiagrams.aws.storage.ElasticBlockStoreEBSSnapshot

#     ElasticBlockStoreEBSVolumediagrams.aws.storage.ElasticBlockStoreEBSVolume

#     ElasticBlockStoreEBSdiagrams.aws.storage.ElasticBlockStoreEBS, EBS (alias)

#     ElasticFileSystemEFSFileSystemdiagrams.aws.storage.ElasticFileSystemEFSFileSystem

#     ElasticFileSystemEFSdiagrams.aws.storage.ElasticFileSystemEFS, EFS (alias)

#     FsxForLustrediagrams.aws.storage.FsxForLustre

#     FsxForWindowsFileServerdiagrams.aws.storage.FsxForWindowsFileServer

#     Fsxdiagrams.aws.storage.Fsx, FSx (alias)

#     MultipleVolumesResourcediagrams.aws.storage.MultipleVolumesResource

#     S3GlacierArchivediagrams.aws.storage.S3GlacierArchive

#     S3GlacierVaultdiagrams.aws.storage.S3GlacierVault

#     S3Glacierdiagrams.aws.storage.S3Glacier

#     SimpleStorageServiceS3BucketWithObjectsdiagrams.aws.storage.SimpleStorageServiceS3BucketWithObjects

#     SimpleStorageServiceS3Bucketdiagrams.aws.storage.SimpleStorageServiceS3Bucket

#     SimpleStorageServiceS3Objectdiagrams.aws.storage.SimpleStorageServiceS3Object

#     SimpleStorageServiceS3diagrams.aws.storage.SimpleStorageServiceS3, S3 (alias)

#     SnowFamilySnowballImportExportdiagrams.aws.storage.SnowFamilySnowballImportExport

#     SnowballEdgediagrams.aws.storage.SnowballEdge

#     Snowballdiagrams.aws.storage.Snowball

#     Snowmobilediagrams.aws.storage.Snowmobile

#     StorageGatewayCachedVolumediagrams.aws.storage.StorageGatewayCachedVolume

#     StorageGatewayNonCachedVolumediagrams.aws.storage.StorageGatewayNonCachedVolume

#     StorageGatewayVirtualTapeLibrarydiagrams.aws.storage.StorageGatewayVirtualTapeLibrary

#     StorageGatewaydiagrams.aws.storage.StorageGateway

#     Storagediagrams.aws.storage.Storage
