import yaml
import subprocess
import time
import os
import sys
values = {}

Vus = "2"
Rate = "1"
Rps = "100"
Duration = "30s"
try:
    Pods = os.environ["DISTRIBUTED_PODS"]
except:
    Pods = "1"

values["Vus"] = Vus
values["Rate"] = Rate
values["Rps"] = Rps
values["Duration"] = Duration
values["Pods"] = Pods

jsScript = sys.argv[1]
mainDir = os.path.dirname(__file__)
######___________________________________________Extracting the main js script

script = ""
with open(jsScript, "r") as k6_script:
    script = "".join(k6_script.readlines())
    values["Script"] = script


######___________________________________________Extracting the IP address

response = (subprocess.check_output(["kubectl", "get", "pods", "-o", "wide", "--namespace", "default"]).decode("utf-8")).split("\n")
for line in response:
    if "dynamic-app" in line:
        pod = line.split()
        values["Ip"] = pod[5]


######___________________________________________Populating the values.yaml file
valuesFile = os.path.join(mainDir, "k6-helm/values.yaml")
with open(valuesFile, "w") as value_file:
    value_file.write(yaml.dump(values))



######___________________________________________Deploying Helm
try:
    time.sleep(2)
    helmDirec = os.path.join(mainDir, "k6-helm")
    if os.system(f"helm install k6 {helmDirec}") != 0:
        print("Error deploying helm.......")
    else:
        print("Helm chart deployed !")
        finished = False
        while True:
            response = (subprocess.check_output(["kubectl", "get", "pods"]).decode("utf-8")).split("\n")
            for line in response:
                if ("k6" in line) and ("initializer" not in line) and ("operator" not in line) and ("starter" not in line):
                    pod = line.split()
                    print(f"Status: {line} : {pod[2]}")
                    if pod[2] == "Completed":
                        results = (subprocess.check_output(["kubectl", "logs", pod[0]]).decode("utf-8"))
                        print(results)
                        finished = True
            if finished :
                break
            time.sleep(30)
finally:
    print("\n\n\n\n........deleting K6 instance")
    os.system("helm uninstall k6")