# Trabalho 04 - Sistema Distribuido
###  Tolerância a Falhas e Monitoramento com Kubernetes + Prometheus

## Objetivo
O objetivo deste trabalho é implantar e monitorar uma aplicação distribuída em um ambiente Kubernetes local, com o uso do Minikube e do Prometheus. A atividade utiliza Deployment, múltiplas réplicas, livenessProbe, controle de recursos de CPU e Horizontal Pod Autoscaler (HPA). Além disso, são realizados testes de deleção de Pods, falha de container, sobrecarga de CPU e interrupção do monitoramento.


# Inicialização do Ambiente

**Observação:** para executar os próximos comandos, é necessário que o Minikube esteja instalado e iniciado no computador. Caso ainda não esteja instalado, realize a instalação antes de prosseguir.

### 1. Acesse a pasta do projeto

No terminal, entre no diretório do projeto:

```bash
Trabalho_SD_04
```

### 2. Construa a imagem do container

Execute:

```bash
docker build -t app-fask-monitoramento:latest .
```

Esse comando constrói a imagem Docker da aplicação a partir do `Dockerfile`.

### 3. Carregue a imagem no Minikube

Após construir a imagem, carregue-a no ambiente do Minikube:

```bash
minikube image load app-fask-monitoramento:latest
```

Dessa forma, o Minikube poderá utilizar a imagem criada pelo Docker para iniciar os Pods.

### 4. Aplique os arquivos Kubernetes

Execute:

```bash
kubectl apply -f k8s/
```

O comando aplica os arquivos presentes na pasta:

```text
k8s/
├── deployment.yaml
├── hpa.yaml
├── prometheus.yaml
└── service.yaml
```

Esses arquivos configuram:

* **Deployment:** cria e mantém os Pods da aplicação.
* **Service:** disponibiliza a aplicação para acesso.
* **HPA:** realiza o escalonamento automático conforme o uso de CPU.
* **Prometheus:** coleta e monitora as métricas do ambiente Kubernetes.

### 5. Verifique os recursos

Confira os Pods:

```bash
kubectl get pods
```

Verifique o HPA:

```bash
kubectl get hpa
```

Inicialmente, a aplicação deverá estar executando com **2 réplicas**.

### 6. Acesse o Minikube Dashboard
Execute o comando:

```bash
minikube dashboard
```
O comando abrirá o Dashboard do Minikube, permitindo visualizar graficamente os recursos do cluster, como Pods, Deployments, Services e ReplicaSets.

# Habilite o Metrics Server

Execute:

```bash
minikube addons enable metrics-server
```

Depois aguarde alguns segundos.



# Ambiente Pronto

Após configurar o Kubernetes, execute os testes abaixo para verificar o funcionamento da aplicação, a recuperação dos Pods e o escalonamento automático.

### Conferir os Pods e ReplicaSets

Verifique os Pods e o ReplicaSet responsáveis pela aplicação:

```bash
kubectl get pods
kubectl get replicasets
```

A aplicação deve estar executando com **2 Pods**.

### Expor a aplicação

Execute:

```bash
minikube service app-monitoramento --url
```

O comando disponibiliza uma URL para acesso à aplicação http://127.0.0.1:xxxxx.


## TESTE 1 — Deleção de Pod

Exclua um dos Pods:

```bash
kubectl delete pod <NOME_DO_POD>
```

Em seguida, acompanhe os Pods:

```bash
kubectl get pods
```

O Kubernetes deverá criar automaticamente um novo Pod para manter as **2 réplicas** definidas no Deployment.


## TESTE 2 — Falha do Container

Utilize a URL obtida anteriormente:

```bash
curl http://127.0.0.1:<PORTA>/crash
```

O comando poderá retornar um erro ou fechar a conexão. Isso é esperado, pois o endpoint `/crash` encerra o processo da aplicação.

Verifique os Pods:

```bash
kubectl get pods
```

Observe a coluna:

```text
RESTARTS
```

O valor deverá aumentar, por exemplo:

```text
0 → 1
```

Isso demonstra que o Kubernetes **reiniciou o container dentro do mesmo Pod**. Diferentemente do teste anterior, o nome do Pod permanece o mesmo e apenas o número de reinicializações aumenta.


## TESTE 3 — Sobrecarga de CPU e HPA

Antes de iniciar a carga, abra um terminal e acompanhe o HPA:

```bash
kubectl get hpa -w
```

Em outro terminal, acompanhe o consumo de CPU dos Pods:

```bash
curl "http://127.0.0.1:<PORTA>/cpu?segundos=60"
```

Durante a execução, volte ao terminal onde o HPA está sendo monitorado e observe a coluna REPLICAS. O número de Pods deverá aumentar conforme o consumo de CPU ultrapassar o limite configurado.

## TESTE 4 — Interrupção do Monitoramento

Para testar a interrupção do monitoramento, primeiro verificamos se o Prometheus está em execução:

```bash
kubectl get pods
```

Em seguida, interrompa temporariamente o Prometheus executando:

```bash
kubectl scale deployment prometheus --replicas=0
```

A aplicação continuará funcionando normalmente, mesmo sem o Prometheus realizando o monitoramento.

Para iniciar o Prometheus novamente, execute:

```bash
kubectl scale deployment prometheus --replicas=1
```

Por fim, verifique se o Pod do Prometheus foi criado novamente



# Acessando a interface do Prometheus

Com o Minikube em execução e o Prometheus iniciado, execute:

```bash
minikube service prometheus --url
```

O comando retornará uma URL semelhante a:

```text
http://127.0.0.1:xxxxx
```

Copie a URL exibida e abra-a no navegador.

A interface web do Prometheus será exibida, permitindo consultar as métricas coletadas do ambiente Kubernetes.

Na interface do Prometheus, acesse a opção **Graph** e execute a consulta:

```promql
up
```

Essa consulta permite verificar se os alvos configurados para monitoramento estão disponíveis.

# Estrutura de Arquivos

```
Trabalho_SD_04
├─ app
│  ├─ main.py
│  └─ requirements.txt
├─ k8s
│  ├─ deployment.yaml
│  ├─ hpa.yaml
│  ├─ prometheus.yaml
│  └─ service.yaml
├─ Dockerfile
└─ README.md

```