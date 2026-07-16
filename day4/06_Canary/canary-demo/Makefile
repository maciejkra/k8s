
build: dep vet build-canary
step-1: dry-run deploy-prod
step-2: dry-run deploy-canary

dep:
	go get github.com/Masterminds/glide
	glide install

vet: 
	go vet ./cmd/main.go

build-canary:
	go build -o ./bin/canary-demo ./cmd/main.go

deploy-prod:
	kubectl apply -f ./deploy/prod-namespace.yaml
	sleep 2
	kubectl apply -f ./deploy/prod-deployment.yaml,./deploy/prod-service.yaml

deploy-canary:
	kubectl apply -f ./deploy/canary-namespace.yaml
	sleep 2
	kubectl apply -f ./deploy/canary-deployment.yaml,./deploy/canary-service.yaml

deploy-route:
	# Weighted routing przez Gateway API (HTTPRoute + ReferenceGrants).
	# Edytuj weight w httproute.yaml żeby zmienić proporcje (100/0 → 80/20 → 50/50 → 20/80 → 0/100).
	kubectl apply -f ./deploy/httproute.yaml

dry-run:
	kubectl apply -f ./deploy/. --dry-run=client

clean-up:
	kubectl delete -f ./deploy/. --ignore-not-found