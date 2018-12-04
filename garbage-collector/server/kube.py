from kubernetes import client, config
import sys, logging

#https://github.com/kubernetes-client/python/blob/master/examples/in_cluster_config.py

logging.basicConfig(level=logging.INFO)

class Kube:

    def __init__(self):
        config.load_incluster_config()
        self.__kube_client = client

    def deleteResources(self,label):
        service_details = self.__kube_client.CoreV1Api().list_namespaced_service('default',label_selector=label )
        deployment_details = self.__kube_client.ExtensionsV1beta1Api().list_namespaced_deployment('default',label_selector=label )
        job_details = self.__kube_client.BatchV1Api().list_namespaced_job('default',label_selector=label)

        # print service_details
        # print deployment_details
        # delete job)
        logging.info("Found {} jobs matching {}...".format(len(job_details.items),label))
        for item in job_details.items:
            name = item.metadata.name
            print "attempting to delete job {}".format(name)
            api_response = self.__kube_client.BatchV1Api().delete_namespaced_job(
            name=name,
            namespace="default",
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5))
            logging.info("-- Deployment {} deleted. status='{}' \n".format(name ,api_response.status))
        print " \n"

        # delete service
        logging.info("Found {} services matching {}...".format(len(service_details.items),label))
        for item in service_details.items:
            name = item.metadata.name
            logging.info("attempting to delete service {}".format(name))
            api_response = self.__kube_client.CoreV1Api().delete_namespaced_service(
            name=name,
            namespace="default",
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5))
            logging.info("Service {} deleted. status='{}' \n".format(name ,api_response.status))
        print " \n"

        # delete deployment
        logging.info("Found {} deployments matching {}...".format(len(deployment_details.items),label))
        for item in deployment_details.items:
            name = item.metadata.name
            logging.info("attempting to delete deployment {}".format(name))
            api_response = self.__kube_client.ExtensionsV1beta1Api().delete_namespaced_deployment(
            name=name,
            namespace="default",
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5))
            logging.info("Deployment {} deleted. status='{}' \n".format(name ,api_response.status))


