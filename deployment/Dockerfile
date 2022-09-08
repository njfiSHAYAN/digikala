FROM alpine/ansible

WORKDIR /deployment

COPY ../ansible /deployment/ansible

COPY ../helmCharts /deployment/helmCharts

COPY ./digi /root/.ssh/digi

ENV ANSIBLE_CONFIG="/deployment/ansible/ansible.cfg"

CMD [ "ansible-playbook", "/deployment/ansible/main.yaml" ]

