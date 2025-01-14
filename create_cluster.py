import subprocess as sb
from time import sleep

def get_ips():
    output = sb.getoutput("kubectl get pods -ocustom-columns=NAME:.metadata.name,IP:.status.podIP")
    output = output.split("\n")
    output.pop(0)
    ips = {} #Stores the hash of Names and IPs of all pods
    for pod in output:
        pod = pod.split("   ")
        ips[pod[0]] = pod[1]

    return ips

sb.run("kubectl apply -f .", shell=True)
print("waiting for 60 seconds...")
sleep(60) #wait for 60 seconds for all the redis pods to working
ips = get_ips()

cmd = "kubectl exec -it redis-cluster-0  -- redis-cli  --cluster-replicas 2 --cluster create "
for pod in ips:
    cmd += ips[pod] + ":6379 "

sb.run("echo 'yes' | "+ cmd, shell=True)