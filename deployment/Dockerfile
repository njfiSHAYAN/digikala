FROM alpine/ansible

WORKDIR /deployment

COPY ansible /deployment/ansible

COPY helmCharts /deployment/helmCharts

COPY deployment/digi /root/.ssh/digi

ENV ANSIBLE_CONFIG="/deployment/ansible/ansible.cfg"

#CMD [ "ansible-playbook", "/deployment/ansible/main.yaml" ]
CMD [ "ping", "google.com", "-c", "10" ]

