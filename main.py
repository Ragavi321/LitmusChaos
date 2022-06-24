import requests
import json
import pprint

baseurl = 'https://api.openweathermap.org/data/2.5/onecall'
lat = '29.3867'
lon = '73.9031'
API_KEY = '456030954b1d645fb1bc07f48ae31b44'
exclude = "hourly,daily"

url1 = baseurl + '?lat=' + lat + '&lon=' + lon + "&exclude=" + exclude + '&appid=' + API_KEY
print(url1)

response = requests.get(url1)
pprint.pprint(response.json())




import requests
import json

url = "http://a61be9f85c8fb47de989a1ad6e2773b3-2105213535.us-east-1.elb.amazonaws.com:9091/auth/login"

payload = json.dumps({
  "username": "admin",
  "password": "litmus"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


url = "http://a61be9f85c8fb47de989a1ad6e2773b3-2105213535.us-east-1.elb.amazonaws.com:9091/api/query"

payload = json.dumps({
  "operationName": "createChaosWorkFlow",
  "variables": {
    "ChaosWorkFlowInput": {
      "workflow_manifest": "{\n  \"apiVersion\": \"argoproj.io/v1alpha1\",\n  \"kind\": \"Workflow\",\n  \"metadata\": {\n    \"name\": \"pod-kill-workflow-100\",\n    \"namespace\": \"litmus\",\n    \"labels\": {\n      \"subject\": \"pod-kill-workflow_litmus\"\n    }\n  },\n  \"spec\": {\n    \"arguments\": {\n      \"parameters\": [\n        {\n          \"name\": \"adminModeNamespace\",\n          \"value\": \"litmus\"\n        }\n      ]\n    },\n    \"entrypoint\": \"custom-chaos\",\n    \"securityContext\": {\n      \"runAsNonRoot\": true,\n      \"runAsUser\": 1000\n    },\n    \"serviceAccountName\": \"argo-chaos\",\n    \"templates\": [\n      {\n        \"name\": \"custom-chaos\",\n        \"steps\": [\n          [\n            {\n              \"name\": \"install-chaos-experiments\",\n              \"template\": \"install-chaos-experiments\"\n            }\n          ],\n          [\n            {\n              \"name\": \"pod-delete\",\n              \"template\": \"pod-delete\"\n            }\n          ],\n          [\n            {\n              \"name\": \"revert-chaos\",\n              \"template\": \"revert-chaos\"\n            }\n          ]\n        ]\n      },\n      {\n        \"name\": \"install-chaos-experiments\",\n        \"inputs\": {\n          \"artifacts\": [\n            {\n              \"name\": \"pod-delete\",\n              \"path\": \"/tmp/pod-delete.yaml\",\n              \"raw\": {\n                \"data\": \"apiVersion: litmuschaos.io/v1alpha1\\ndescription:\\n  message: |\\n    Deletes a pod belonging to a deployment/statefulset/daemonset\\nkind: ChaosExperiment\\nmetadata:\\n  name: pod-delete\\n  labels:\\n    name: pod-delete\\n    app.kubernetes.io/part-of: litmus\\n    app.kubernetes.io/component: chaosexperiment\\n    app.kubernetes.io/version: 2.0.0\\nspec:\\n  definition:\\n    scope: Namespaced\\n    permissions:\\n      - apiGroups:\\n          - \\\"\\\"\\n          - apps\\n          - apps.openshift.io\\n          - argoproj.io\\n          - batch\\n          - litmuschaos.io\\n        resources:\\n          - deployments\\n          - jobs\\n          - pods\\n          - pods/log\\n          - replicationcontrollers\\n          - deployments\\n          - statefulsets\\n          - daemonsets\\n          - replicasets\\n          - deploymentconfigs\\n          - rollouts\\n          - pods/exec\\n          - events\\n          - chaosengines\\n          - chaosexperiments\\n          - chaosresults\\n        verbs:\\n          - create\\n          - list\\n          - get\\n          - patch\\n          - update\\n          - delete\\n          - deletecollection\\n    image: litmuschaos/go-runner:2.0.0\\n    imagePullPolicy: Always\\n    args:\\n      - -c\\n      - ./experiments -name pod-delete\\n    command:\\n      - /bin/bash\\n    env:\\n      - name: TOTAL_CHAOS_DURATION\\n        value: \\\"15\\\"\\n      - name: RAMP_TIME\\n        value: \\\"\\\"\\n      - name: FORCE\\n        value: \\\"true\\\"\\n      - name: CHAOS_INTERVAL\\n        value: \\\"5\\\"\\n      - name: PODS_AFFECTED_PERC\\n        value: \\\"\\\"\\n      - name: LIB\\n        value: litmus\\n      - name: TARGET_PODS\\n        value: \\\"\\\"\\n      - name: SEQUENCE\\n        value: parallel\\n    labels:\\n      name: pod-delete\\n      app.kubernetes.io/part-of: litmus\\n      app.kubernetes.io/component: experiment-job\\n      app.kubernetes.io/version: 2.0.0\\n\"\n              }\n            }\n          ]\n        },\n        \"container\": {\n          \"args\": [\n            \"kubectl apply -f /tmp/pod-delete.yaml -n {{workflow.parameters.adminModeNamespace}} |  sleep 30\"\n          ],\n          \"command\": [\n            \"sh\",\n            \"-c\"\n          ],\n          \"image\": \"litmuschaos/k8s:latest\"\n        }\n      },\n      {\n        \"name\": \"pod-delete\",\n        \"inputs\": {\n          \"artifacts\": [\n            {\n              \"name\": \"pod-delete\",\n              \"path\": \"/tmp/chaosengine-pod-delete.yaml\",\n              \"raw\": {\n                \"data\": \"apiVersion: litmuschaos.io/v1alpha1\\nkind: ChaosEngine\\nmetadata:\\n  namespace: \\\"{{workflow.parameters.adminModeNamespace}}\\\"\\n  generateName: pod-delete\\n  labels:\\n    instance_id: 6dfb1693-4e3d-4b9b-957b-9f61746bd128\\n    context: pod-delete_litmus\\n    workflow_name: pod-kill-workflow-1655991677\\nspec:\\n  appinfo:\\n    appns: default\\n    applabel: app=nginx\\n    appkind: deployment\\n  jobCleanUpPolicy: retain\\n  engineState: active\\n  chaosServiceAccount: litmus-admin\\n  experiments:\\n    - name: pod-delete\\n      spec:\\n        components:\\n          env:\\n            - name: TOTAL_CHAOS_DURATION\\n              value: \\\"30\\\"\\n            - name: CHAOS_INTERVAL\\n              value: \\\"10\\\"\\n            - name: FORCE\\n              value: \\\"false\\\"\\n            - name: PODS_AFFECTED_PERC\\n              value: \\\"\\\"\\n        probe: []\\n  annotationCheck: \\\"false\\\"\\n\"\n              }\n            }\n          ]\n        },\n        \"container\": {\n          \"args\": [\n            \"-file=/tmp/chaosengine-pod-delete.yaml\",\n            \"-saveName=/tmp/engine-name\"\n          ],\n          \"image\": \"litmuschaos/litmus-checker:latest\"\n        }\n      },\n      {\n        \"name\": \"revert-chaos\",\n        \"container\": {\n          \"image\": \"litmuschaos/k8s:latest\",\n          \"command\": [\n            \"sh\",\n            \"-c\"\n          ],\n          \"args\": [\n            \"kubectl delete chaosengine -l 'instance_id in (6dfb1693-4e3d-4b9b-957b-9f61746bd128, )' -n {{workflow.parameters.adminModeNamespace}} \"\n          ]\n        }\n      }\n    ],\n    \"podGC\": {\n      \"strategy\": \"OnWorkflowCompletion\"\n    }\n  }\n}",
      "cronSyntax": "",
      "workflow_name": "pod-kill-workflow-100",
      "workflow_description": "Custom Chaos Workflow",
      "isCustomWorkflow": True,
      "weightages": [
        {
          "experiment_name": "pod-delete",
          "weightage": 10
        }
      ],
      "project_id": "5539c642-f80f-443d-a21b-406379f8df48",
      "cluster_id": "f3e5ba30-98a4-4821-92b6-00efcd7cb3c2"
    }
  },
  "query": "mutation createChaosWorkFlow($ChaosWorkFlowInput: ChaosWorkFlowInput!) {\n  createChaosWorkFlow(input: $ChaosWorkFlowInput) {\n    workflow_id\n    cronSyntax\n    workflow_name\n    workflow_description\n    isCustomWorkflow\n    __typename\n  }\n}\n"
})
headers = {
  'authorization': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NTYxMzAyMTcsInJvbGUiOiJhZG1pbiIsInVpZCI6IjVkMmM4YzMyLTlhMzUtNGI3Yy04ZGE4LTY0ZDM5OWU3NTE5ZCIsInVzZXJuYW1lIjoiYWRtaW4ifQ.PkC1eT0ihMcVbr3hpnnQTB3ihXhT19qDrEIiscOopZHVne41ivPyS8OWB5yHtmPu3ineQOaBjcinG35KJQ8j3g',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


