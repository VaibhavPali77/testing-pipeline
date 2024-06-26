FROM ubuntu:jammy
RUN apt update
RUN apt install nano
RUN apt install curl -y

# Installing python
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip3 install kubernetes

# Installing kubectl 
RUN apt-get install -y apt-transport-https ca-certificates curl
RUN curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
RUN chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg
RUN echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list
RUN chmod 644 /etc/apt/sources.list.d/kubernetes.list
RUN apt update
RUN apt install -y kubectl

# Installing helm
RUN curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | tee /usr/share/keyrings/helm.gpg > /dev/null
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | tee /etc/apt/sources.list.d/helm-stable-debian.list
RUN apt update
RUN apt install helm -y

# RUN mkdir framework
# WORKDIR /framework

CMD ["sleep", "infinity"]
