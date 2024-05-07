import yaml
import subprocess
import time
import os
import sys
values = {}

Vus = "2"
Rate = "2"
Rps = "2000"
Duration = "120s"

try:
    Pods = os.environ["DISTRIBUTED_PODS"]
except:
    Pods = "2"

values["Vus"] = Vus
values["Rate"] = Rate
values["Rps"] = str(float(Rps)/float(Vus))
values["Duration"] = Duration
values["Pods"] = Pods

pythonScript = sys.argv[1]
mainDir = os.path.dirname(__file__)

helmFolder = sys.argv[2]

print("Starting process.......")
######___________________________________________Extracting the main python script

script = ""
with open(pythonScript, "r") as locust_script:
    script = "".join(locust_script.readlines())
    values["Script"] = script
print("Extracted script")


######___________________________________________Extracting the IP address

response = (subprocess.check_output(["kubectl", "get", "pods", "-o", "wide", "-n", "default"]).decode("utf-8")).split("\n")
for line in response:
    if "dynamic-app" in line:
        pod = line.split()
        values["Ip"] = pod[5]
print(f"Extracted IP : {values['Ip']}")


######___________________________________________Populating the values.yaml file
valuesFile = os.path.join(mainDir, f"{helmFolder}/values.yaml")
with open(valuesFile, "w") as value_file:
    value_file.write(yaml.dump(values))
print("Populated values.yaml")


######___________________________________________Deploying Helm
try:
    time.sleep(2)
    helmDirec = os.path.join(mainDir, helmFolder)
    if os.system(f"helm install locust {helmDirec}") != 0:
        print("Error deploying helm.......")
    else:
        print("Helm chart deployed !")
        finished = False
        while True:
            response = (subprocess.check_output(["kubectl", "get", "pods"]).decode("utf-8")).split("\n")
            for line in response:
                if "locust-master" in line:
                    pod = line.split()
                    print(f"Status: {line}")
                    if pod[2] == "Completed":
                        results = (subprocess.check_output(["kubectl", "logs", pod[0]]).decode("utf-8"))
                        # if "master" in line:
                        #     print(results)
                        print(results)
                        print("\n\n\n\n\n\n")
                        finished = True
            if finished :
                break
            time.sleep(30)
finally:
    print("\n\n........deleting locust instance")
    os.system("helm uninstall locust")