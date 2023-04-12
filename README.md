# **Elastic Stack**

Repositório contendo os arquivos de configuração do Elastic Stack para rodar em Kubernetes.

<br>

## **ATENÇÃO**

O código armazenado neste repositório não necessariamente adere às normas de qualidade para sistemas de produção.
Portanto, caso deseje utilizar o código para fins de produção, é necessário que o mesmo seja revisado e testado.

<br>

## **Requisitos mínimos:**
- Minikube: v1.26.1
- Kubectl: v1.24.4

<br>

## HOW-TO: Configurando o ambiente
<br>

### 1. Aumentando quantidade de memória, vCPU, e armazenamento no minikube:
```bash
minikube config set memory 8192 && minikube config set cpus 4 && minikube config set disk-size 50g
```

### 2. Iniciando o minikube:
```bash
minikube start
```

### 3. Instalando o Elastic Cloud for Kubernetes (ECK) CRD:
```bash
kubectl create -f https://download.elastic.co/downloads/eck/2.4.0/crds.yaml
```

### 4. Instalando o operador ECK:
```bash
kubectl apply -f https://download.elastic.co/downloads/eck/2.4.0/operator.yaml
```

### 5. Configurando um cluster Elasticsearch:
```bash
kubectl apply -f kubernetes/elasticsearch.yml
```

### 6. Configurando um cluster Kibana:
```bash
kubectl apply -f kubernetes/kibana.yml
```

<br>

## HOW-TO: Acessando o Kibana e Elasticsearch

<br>

### 1. Abrindo um túnel de conexão para o cluster:
```bash
minikube tunnel
```

### 2. Recuperando a senha do usuário elastic:
```bash
kubectl get secret dev-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode; echo
```

### 3. Verificando o IP do cluster Elasticsearch:
```bash
kubectl get service dev-es-http
```

### 4. Verificando o IP do cluster Kibana:
```bash
kubectl get service dev-kb-http
```
