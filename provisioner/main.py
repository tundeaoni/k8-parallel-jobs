#!/usr/bin/env python
import sys , os , kube, util , constants

def provision():
    # check for configuration file
    config_file = constants.CONFIG_FILE
    environments_config_key = constants.ENVIRONMENTS_CONFIG_KEY
    exposed_port_key = constants.EXPOSED_PORT_KEY
    exposed_port_to_job_key = constants.EXPOSED_PORT_TO_JOB_KEY
    deployment_suffix = constants.DEPLOYMENT_SUFFIX
    services_suffix = constants.SERVICES_SUFFIX
    job_suffix = constants.JOBS_SUFFIX
    garbage_collector = constants.GARBAGE_COLLECTOR
    garbage_collector_url = constants.GARBAGE_COLLECTOR_URL
    auth_config_file_name = constants.AUTH_CONFIG_FILE_NAME
    env_config_key = constants.ENV_KEY

    if os.path.isfile(config_file) == False:
        print "config file (config.yaml) missing in current directory"
        sys.exit(1)

    if os.path.isfile(auth_config_file_name) == True:
        print "Setting config to auth to private repository"
        auth_config = util.fromYaml(auth_config_file_name)
        server = auth_config[constants.AUTH_SERVER_KEY]
        username = auth_config[constants.AUTH_USER_NAME_KEY]
        password = auth_config[constants.AUTH_PASSWORD_KEY]
        email = auth_config[constants.AUTH_EMAIL_KEY]
        kube.auth_docker_repo(server, username, password, email)


    # load config file
    config = util.fromYaml(config_file)
    if environments_config_key not in config:
        print "No environments have been defined in {}".format(config_file)
        sys.exit(0)

    for environment in config[environments_config_key]:
        environment_details = config[environments_config_key][environment]
        exposed_port = environment_details[exposed_port_key]
        exposed_port_to_job = environment_details[exposed_port_to_job_key]
        envs = {}
        if env_config_key in environment_details:
            envs = environment_details[env_config_key]

        values = {
            "name": environment , \
            "service_suffix": services_suffix , \
            "deployment_suffix": deployment_suffix ,\
            "job_suffix": job_suffix ,\
            "group_id": environment , \
            "job_envs": envs ,\
            "exposed_ports": exposed_port ,\
            "garbage_collector": garbage_collector ,\
            "garbage_collector_url": garbage_collector_url , \
            "exposed_port_to_job": exposed_port_to_job, \
            "argument_sets": environment_details[constants.ARGS_KEY]
        }

            # create garabage collector
        print "-- Creating garabage collector"
        kube.create_from_file(constants.DAEMON_SET_CONFIG_LOCATION)

        # create service
        print "-- Creating service for {}".format(environment)
        svc = util.render(constants.SERVICE_TEMPLATE , values)
        # start up service
        kube.start(svc)

        # create deployment
        print "-- Creating deployment for {}".format(environment)
        deployment = util.render(constants.DEPLOYMENT_TEMPLATE , values)
        # start up deployment
        kube.start(deployment)

        # create job
        print "-- Creating job for {}".format(environment)
        job = util.render(constants.JOB_TEMPLATE , values)
        # start up job
        kube.start(job)

def delete_all(environment):
    label = ""
    if environment != "":
        label = "group_id={}".format(environment)
    kube.delete_all(label)

def check_dependency(name):
    if util.is_tool(name) == False:
        print("Error: {} is a requiste to run this tool.".format(name))
        sys.exit(1)


# generate deployment , service then create job

if __name__ == "__main__":
    if len(sys.argv[1:]) == 0 and type(0):
        util.usage()
        sys.exit(0)

    for dependency in ["kubectl"]:
        check_dependency(dependency)

    subCommand = sys.argv[1]
    args = sys.argv[2:]

    if subCommand in ("help"):
        util.usage()
    elif subCommand in ("provision"):
        provision()
    elif subCommand in ("demolish"):
        environment = ""
        if len(args) > 0:
            environment = args[0]
        delete_all(environment)
    else:
        print "'" + subCommand + "' is not a recognised sub-command. Use the help command to see available sub-commands  \n"