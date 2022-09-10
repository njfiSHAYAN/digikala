FROM alpine/ansible

WORKDIR /deployment

COPY ansible /deployment/ansible

COPY helmCharts /deployment/helmCharts

RUN chmod 400 deployment/digi

COPY deployment/digi /root/.ssh/digi

ENV ANSIBLE_CONFIG="/deployment/ansible/ansible.cfg"

ENV ANSIBLE_HOST_KEY_CHECKING=False

CMD [ "ansible-playbook", "/deployment/ansible/main.yaml" ]

