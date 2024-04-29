# import yaml
# import subprocess
# import time
# import os
# import sys

# vus = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
# throughputs = [500]

# for i in range(10):
#     for j in range(10):
#         values = {}
#         Vus = vus[j]
#         Rate = "1"
#         Rps = throughputs[i]
#         Duration = 300
#         Pods = "1"

#         values["Vus"] = Vus
#         values["Rate"] = Rate
#         values["Rpm"] = Rps*60
#         values["Duration"] = Duration
#         values["Pods"] = Pods

#         xmlScript = sys.argv[1]
#         mainDir = os.path.dirname(__file__)
#         ######___________________________________________Extracting the main js script

#         script = ""
#         with open(xmlScript, "r") as jmeter_script:
#             script = "".join(jmeter_script.readlines())
#             values["Script"] = script


#         ######___________________________________________Extracting the IP address

#         response = (subprocess.check_output(["kubectl", "get", "pods", "-o", "wide"]).decode("utf-8")).split("\n")
#         for line in response:
#             if "dynamic-app" in line:
#                 pod = line.split()
#                 values["Ip"] = pod[5]


#         ######___________________________________________Populating the values.yaml file
#         valuesFile = os.path.join(mainDir, "jmeter-helm/values.yaml")
#         with open(valuesFile, "w") as value_file:
#             value_file.write(yaml.dump(values))



#         ######___________________________________________Deploying Helm
#         try:
#             time.sleep(2)
#             helmDirec = os.path.join(mainDir, "jmeter-helm")
#             if os.system(f"helm install jmeter {helmDirec}") != 0:
#                 print("Error deploying helm.......")
#             else:
#                 print("Helm chart deployed !")
#                 finished = False
#                 while True:
#                     response = (subprocess.check_output(["kubectl", "get", "pods"]).decode("utf-8")).split("\n")
#                     for line in response:
#                         if "jmeter" in line:
#                             pod = line.split()
#                             print(f"Status: {line}")
#                             if pod[2] == "Completed":
#                                 results = (subprocess.check_output(["kubectl", "logs", pod[0]]).decode("utf-8"))
#                                 print(results)
#                                 # with open(f"jmeter_{Rps}rps_{Vus}threads.txt", "w") as resultFile:
#                                 #     resultFile.write(results)
#                                 finished = True
#                     if finished :
#                         break
#                     time.sleep(30)
#         finally:
#             print("\n\n\n\n........deleting jmeter instance")
#             os.system("helm uninstall jmeter")



import yaml
import subprocess
import time
import os
import sys

values = {}
Vus = 2
Rate = "1"
Rps = 500
Duration = 30
try:
    Pods = os.environ["DISTRIBUTED_PODS"]
except:
    Pods = "1"

values["Vus"] = Vus
values["Rate"] = Rate
values["Rpm"] = Rps*60
values["Duration"] = Duration
values["Pods"] = Pods

xmlScript = sys.argv[1]
mainDir = os.path.dirname(__file__)
masterHelm = sys.argv[2]
workerHelm = sys.argv[3]

print("Master helm :- ", masterHelm)
print("Worker helm :- ", workerHelm)

######___________________________________________Extracting the main js script

script = ""
with open(xmlScript, "r") as jmeter_script:
    script = "".join(jmeter_script.readlines())
    values["Script"] = script


######___________________________________________Extracting the IP address

response = (subprocess.check_output(["kubectl", "get", "pods", "-o", "wide", "-n", "default"]).decode("utf-8")).split("\n")
for line in response:
    if "dynamic-app" in line:
        pod = line.split()
        values["Ip"] = pod[5]


######___________________________________________Populating the worker values.yaml file
valuesFile = f"{workerHelm}/values.yaml"
with open(valuesFile, "w") as value_file:
    value_file.write(yaml.dump(values))


try:
    time.sleep(2)
    ######_______________________________________Deploying worker Helm
    helmDirec = workerHelm
    print("DIRECTORY :-", helmDirec)
    if os.system(f"helm install jmeter-workers {helmDirec}") != 0:
        print("Error deploying helm.......")
        raise Exception("Error deploying worker helm.......")
    else:
        print("Worker Helm chart deployed !")
    time.sleep(10)


    ######_______________________________________Check if all the workers are running
    while True:
        response = (subprocess.check_output(["kubectl", "get", "pods", "-o", "wide"]).decode("utf-8")).split("\n")
        exit_loop = True
        for line in response:
            if "jmeter" in line:
                pod = line.split()
                if pod[2] != "Running":
                    exit_loop = False
        if exit_loop:
            break
                

    WorkerIps = []
    response = (subprocess.check_output(["kubectl", "get", "pods", "-o", "wide"]).decode("utf-8")).split("\n")
    for line in response:
        if "jmeter" in line:
            pod = line.split()
            WorkerIps.append(pod[5])
    values["WorkerIps"] = ",".join(WorkerIps)


    ####_________________________________________Populating the master values.yaml file
    valuesFile = f"{masterHelm}/values.yaml"
    with open(valuesFile, "w") as value_file:
        value_file.write(yaml.dump(values))

    ######_______________________________________Deploying worker Helm
    helmDirec = masterHelm
    if os.system(f"helm install jmeter-master {helmDirec}") != 0:
        print("\n\nError deploying helm.......")
    else:
        print("\n\nMaster Helm chart deployed !")
        finished = False
        while True:
            response = (subprocess.check_output(["kubectl", "get", "pods"]).decode("utf-8")).split("\n")
            for line in response:
                if "jmeter-master" in line:
                    pod = line.split()
                    print(f"Status: {line}")
                    if pod[2] == "Completed":
                        results = (subprocess.check_output(["kubectl", "logs", pod[0]]).decode("utf-8"))
                        print(results)
                        finished = True
            if finished :
                break
            time.sleep(30)
finally:
    print("\n\n\n\n........deleting jmeter instance")
    os.system("helm uninstall jmeter-workers")
    os.system("helm uninstall jmeter-master")