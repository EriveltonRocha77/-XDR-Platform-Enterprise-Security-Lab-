```markdown
# 🛡️ XDR Neo-Platform | Enterprise Security Lab

**Plataforma unificada de Extended Detection and Response (XDR) e Inteligência Cibernética Operacional**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

> Laboratório de segurança ofensiva e defensiva com algoritmos reais de detecção, resposta e inteligência cibernética.  
> Ambiente completamente isolado via microserviços orquestrados por Docker Compose.

---

## 🎯 Visão Geral

A **XDR Neo-Platform** não é um simulador superficial.  
A maioria das funcionalidades da interface aciona **algoritmos reais** de análise estatística, pattern matching e engenharia reversa implementados no núcleo da API.

Foi desenvolvida com o objetivo de simular um ambiente de SOC (Security Operations Center) completo, unindo capacidades de **Blue Team** e **Red Team** em um único laboratório controlado.

### Principais Capacidades

| Capacidade                        | Descrição Técnica                                      | Tipo          |
|-----------------------------------|--------------------------------------------------------|---------------|
| Extended Detection & Response     | Correlação de eventos multi-fonte                      | Blue Team     |
| SAST (Static Analysis)            | Análise de código via AST (credenciais, injeções)      | Blue Team     |
| DAST (Dynamic Analysis)           | Fuzzing web + detecção de LFI                          | Blue Team     |
| Cloud / IaC Audit                 | Validação de containers e YAML (pods privilegiados)    | Blue Team     |
| OSINT + IOC Correlation           | Georreferenciamento + listas negras (Spamhaus)         | Blue Team     |
| RASP (Runtime Protection)         | Bloqueio de `globals()` e builtins perigosos           | Blue Team     |
| DNS Tunneling Detection           | Detecção via Entropia de Shannon                       | Blue Team     |
| Anomaly Detection                 | Z-Score para comportamento ransomware-like            | Blue Team     |
| Attack Path Mapper                | Mapeamento de privilégios (lógica estilo BloodHound)   | Red Team      |
| Hash Cracker                      | Ataque de dicionário (SHA/MD5)                         | Red Team      |
| WAF + Attack Simulator            | Proteção web + geração controlada de tráfego malicioso | Dual          |

---

## 🏗️ Arquitetura

```text
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend Tático (HUD)                       │
│              HTML / CSS / JS  →  Porta 8080                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                   Backend SIEM (FastAPI)                        │
│              Orquestração + Data Lake  →  Porta 8000            │
└──────┬──────────────┬──────────────┬──────────────┬─────────────┘
       │              │              │              │
┌──────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
│   SAST     │  │   DAST    │  │   Cloud   │  │    WAF    │
│  (AST)     │  │ (Fuzzing) │  │  (IaC)    │  │  Engine   │
└────────────┘  └───────────┘  └───────────┘  └─────┬─────┘
                                                    │
                                              ┌─────▼─────┐
                                              │  Attack   │
                                              │ Simulator │
                                              └───────────┘
```

### Serviços Docker

| Serviço             | Porta  | Função                              |
|---------------------|--------|-------------------------------------|
| `backend`           | 8000   | API principal + SIEM                |
| `xdr-gui`           | 8080   | Interface web tática                |
| `waf-engine`        | 8081   | Web Application Firewall            |
| `sast`              | -      | Análise estática de código          |
| `dast`              | -      | Testes dinâmicos                    |
| `cloud`             | -      | Auditoria de configurações          |
| `attack-simulator`  | -      | Geração de tráfego malicioso        |

---

## 🛠️ Módulos Principais

### 1. Análise de Inteligência (SIEM)
- Painel central de telemetria em tempo real
- SAST com AST (detecção de credenciais hardcoded e injeções)
- DAST com fuzzing e detecção de LFI
- Auditoria Cloud/IaC (pods privilegiados, configurações inseguras)
- Correlação de IOCs via OSINT
- Heurísticas de resposta automática (SOC Analyst AI)

### 2. Contra-Medidas Ativas (EDR / RASP)
- **RASP Shield** → Proteção em runtime
- **Network Hex Hunter** → Detecção de padrões de buffer overflow
- **YARA Memory Scan** → Pattern matching em memória
- **DNS Tunneling Detector** → Entropia de Shannon
- **Anomaly Engine** → Z-Score para comportamento anômalo

### 3. Laboratório Ofensivo
- **Attack Path Mapper** → DFS estilo BloodHound
- **Hash Cracker** → Ataque de dicionário

---

## 🚀 Como Executar

### Pré-requisitos
- Docker
- Docker Compose

### Subir o ambiente

```bash
# Clone o repositório
git clone https://github.com/EriveltonRocha77/-XDR-Platform-Enterprise-Security-Lab-.git
cd "-XDR-Platform-Enterprise-Security-Lab-/landingpage erivelton/sec-analyzers-lab"

# Pare containers antigos (se existirem)
docker-compose down

# Build e suba todos os serviços
docker-compose up -d --build
```

### Acessos

| Serviço          | URL                        |
|------------------|----------------------------|
| Interface Web    | http://localhost:8080      |
| API Backend      | http://localhost:8000      |
| WAF              | http://localhost:8081      |

---

## 📸 Interface

> Estética: HUD militar / Cyberpunk (CRT, neon, tipografia tática)

*(Adicione aqui prints da interface depois de rodar o projeto)*

- Painel principal de telemetria
- Módulo SAST em ação
- Detecção de anomalias
- Attack Path Mapper

---

## 🧰 Stack Tecnológica

- **Backend:** Python 3.11+ · FastAPI
- **Análise:** AST · YARA · Z-Score · Shannon Entropy
- **Frontend:** HTML5 · CSS3 · JavaScript (vanilla)
- **Infraestrutura:** Docker · Docker Compose
- **Segurança:** WAF customizado · RASP · OSINT

---

## 📁 Estrutura do Projeto

```text
sec-analyzers-lab/
├── backend/          # API principal (FastAPI + SIEM)
├── sast/             # Motor de análise estática
├── dast/             # Motor de testes dinâmicos
├── cloud/            # Auditoria de configurações
├── waf/              # Web Application Firewall
├── bot/              # Attack Simulator
├── gui/              # Interface web tática
├── tests/            # Testes
├── docker-compose.yml
└── Dockerfile
```

---

## 🎓 Aprendizados

Este projeto me permitiu aplicar na prática conceitos de:

- Arquitetura de microserviços orientada a segurança
- Correlação de eventos (SIEM)
- Detecção de anomalias estatísticas
- Proteção em runtime (RASP)
- Orquestração com Docker Compose
- Integração entre ferramentas ofensivas e defensivas

---

## 👨‍💻 Autor

**Erivelton da Rocha Silva**  
Estudante de Engenharia de Software e Segurança da Informação  
📍 Sertãozinho / SP - Brasil

- 💼 [LinkedIn](https://www.linkedin.com/in/eriveltonrocha18)
- 🌐 [Portfólio](https://eriveltonrochaportifolio1.pages.dev)
- 🐙 [GitHub](https://github.com/EriveltonRocha77)
- 📧 eriveltoncurriculo@gmail.com

---

## 📄 Licença

Este projeto está sob a licença MIT.
```
