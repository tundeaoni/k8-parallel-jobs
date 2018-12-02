import os ,sys, util
def start(manifest):
    temp_file = os.getcwd() + "/temp.yml"
    manifest.dump(temp_file)
    os.system("kubectl apply -f {}".format(temp_file))
    os.remove(temp_file)

def delete_all():
    os.system("kubectl delete $(kubectl get all --namespace=default | awk '{print $1}' | grep -v \"NAME\")")