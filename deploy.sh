#!/bin/bash
#
echo "[`date`] Deploying docs to server"
cd devops/ansible
# first install python (or ansible fails)
#ansible-playbook ./prepare_host.yml -i inv-dev -s
# fuck about with nginx: certbot, dhparams
#ansible-playbook ./pre_deploy_service.yml -i inv-dev -s
ansible-playbook ./deploy_otpazk.yml -i inv-dev -s
echo "[`date`] Finished deploying to server"
