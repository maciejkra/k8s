#!/bin/sh
while :
do

	spec=$(kubectl get podcreators example-pod-creator -o json | jq ".spec") 
	podname=$(echo $spec | jq -r ".createPod")
	svcname=$(echo $spec | jq -r ".createSvc")
	imagename=$(echo $spec | jq -r ".imageName")
	echo $podname
	echo $svcname
	echo $imagename
	echo "Checking $podname"
	kubectl get pods | grep -q "$podname"
	if [ $? -eq 1 ]
	then
		kubectl run $podname --image=$imagename
		kubectl expose pod $podname --type=NodePort --name=$svcname --port=80
	else
		echo "$podname found"
	fi
	sleep 30
done