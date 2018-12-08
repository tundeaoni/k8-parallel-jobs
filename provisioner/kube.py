import os ,sys, util

def start(manifest):
    temp_file = os.getcwd() + "/temp.yml"
    manifest.dump(temp_file)
    os.system("kubectl apply -f {}".format(temp_file))
    # os.system("cat {}".format(temp_file))
    os.remove(temp_file)

def create_from_file(location):
    os.system("kubectl apply -f {}".format(location))

def auth_docker_repo(server, username, password, email):
    os.system("kubectl create secret docker-registry regcred --docker-server={} --docker-username={} --docker-password={} --docker-email={}".format(server,username, password, email))

def delete_all(label):
    if label != "":
        label = "-l{}".format(label)
    os.system("kubectl delete $(kubectl get all {} --namespace=default | awk '{{print $1}}' | grep -v \"NAME\")".format(label))