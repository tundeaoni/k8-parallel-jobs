import os

CONFIG_FILE = os.getcwd() + "/config.yml"
TEMPLATES = os.getcwd() + "/templates/"
ENVIRONMENTS_CONFIG_KEY = "environments"
SERVICE_TEMPLATE = TEMPLATES + "service.jinja"
DEPLOYMENT_TEMPLATE = TEMPLATES + "deployment.jinja"
JOB_TEMPLATE = TEMPLATES + "job.jinja"
DEPLOYMENT_SUFFIX = "-deployment"
SERVICES_SUFFIX = "-svc"
JOBS_SUFFIX = "-job"
EXPOSED_PORT_KEY = "exposed_port"
ARGS_KEY = "args_sets"