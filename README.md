### Introduction
Kubernetes resoures are logically grouped with the intention to independently reference and management them.
<!-- 
├── README.md
├── garbage-collector
│   ├── Dockerfile
│   └── server
│       ├── kube.py
│       ├── requirements.txt
│       └── server.py
└── provisioner
    ├── auth-config.example.yml
    ├── config.yml
    ├── constants.py
    ├── constants.pyc
    ├── daemon_set
    │   ├── daemonset.yaml
    │   ├── rbac-garbage-collector.yml
    │   └── service.yaml
    ├── kube.py
    ├── main.py
    ├── requirements.txt
    ├── templates
    │   ├── deployment.jinja
    │   ├── job.jinja
    │   └── service.jinja
    ├── util.py -->

### Requirements
- Kubectl 
- python 2.7

### Set up
- clone repository
- cd into /repository-path/provisioner/
- run `pip install requirements.txt`
- configure kubectl to connect to kubernetes cluster of interest
- run `./main.py help` to view available commands

### Available commands
- `./main.py provision`
    setups logical groups of kubernetes resources as defined in the `/repository-path/provisioner/config.yaml` file. 
- `./main.py demolish`
    The demolish command deletes all the created resources in a kubernetes cluster. To delete only a single group, specify the name of the group in the command i.e `./main.py demolish environment-name-as-defined-in-config`

### Garbage Collector 
The garbage collector is a small application deployed on provisioning who is responsible for cleaning up resource groups(environments) which have achieved thier goal. Basically a resource from a group just notifies the garbage collector about task completition and it cleans up the all the resources in the group. The notification is done using a http POST request(further details on this can be found in the MISC section). Kubernetes configurations related to the deamonset can be found in the `provisioner/daemon_set` folder.

### MISC
- There is support for triggering the cleaning up of a group/environment from an of the resources within the environment. To do this simply make POST request using the enviroment variable `$GARBAGE_COLLECTOR_URL` (this environment variable is automatically injected on setup) with payload `{  "label": "group_id=$GROUP_ID" }`
the value of the `$GROUP_ID` is also injected automatically on setup.
The curl request will look like this
`curl -X POST $GARBAGE_COLLECTOR_URL -H 'content-type: application/json' -d "{  \"label\": \"group_id=$GROUP_ID\" }"`
- For using images in a private docker repository create a file named `auth-config.yml` from the file `auth-config.example.yml` and update with the configuration with required values.
- The templates used for the creation of groups/environments can be found in the `provisioner/template` folder, changes made here would reflect in the definition of resources on subsequent creation.
- The code for the garbage-collector can be found in the `garbage-collector`.
