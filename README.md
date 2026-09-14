# 🛡️ XDR Neo-Platform | Enterprise Security Lab

**Plataforma unificada de Extended Detection and Response (XDR) e Inteligência Cibernética Operacional**

Laboratório de segurança ofensiva e defensiva projetado para análise real de ameaças, detecção, resposta e inteligência. Combina motores de análise estática/dinâmica, correlação de IOCs, proteção em runtime e simulações de ataque em um ambiente isolado via Docker.

> **Estética:** Interface tática estilo HUD militar / Cyberpunk (CRT, neon e tipografia assíncrona)

---

## 🎯 Visão Geral

A XDR Neo-Platform não é um simulador superficial. A maioria das funcionalidades da interface aciona **algoritmos reais** de análise estatística, pattern matching e engenharia reversa implementados no núcleo da API.

O ambiente roda completamente isolado através de microserviços orquestrados por Docker Compose.

### Principais Capacidades

- Detecção e resposta estendida (XDR)
- Análise estática de código (SAST)
- Testes dinâmicos de aplicações web (DAST)
- Auditoria de configurações cloud/Kubernetes
- Correlação de IOCs via OSINT
- Proteção em runtime (RASP)
- Detecção de exfiltração via DNS tunneling
- Análise de anomalias com Z-Score
- Mapeamento de caminhos de ataque (estilo BloodHound)
- Quebra de hashes (simulação)

---

## 🏗️ Arquitetura

| Componente              | Tecnologia          | Função                                      |
|-------------------------|---------------------|---------------------------------------------|
| **Frontend Tático**     | HTML/CSS/JS puro    | HUD militar com estética cyberpunk         |
| **Backend SIEM**        | Python + FastAPI    | Orquestração, data lake e roteamento       |
| **Micro-operadores**    | Python + AST/YARA   | Análise paralela de código, memória e rede |
| **WAF Engine**          | Python              | Proteção web e simulação de ataques        |
| **Attack Simulator**    | Python              | Geração controlada de tráfego malicioso    |

### Serviços Docker

- `backend` → API principal (porta 8000)
- `waf-engine` → WAF (porta 8081)
- `attack-simulator` → Simulador de ataques
- `sast` / `dast` / `cloud` → Motores de análise
- `xdr-gui` → Interface web (porta 8080)

---

## 🛠️ Módulos Principais

### 1. Análise de Inteligência (SIEM)

| Módulo                  | Descrição |
|-------------------------|-----------|
| **Painel Central**      | Concentrador de telemetria em tempo real |
| **SAST**                | Análise estática via AST (credenciais hardcoded, injeções) |
| **DAST**                | Fuzzing web (HEAD requests, LFI) contra o WAF |
| **Cloud/IaC Audit**     | Validação de containers e YAML (pods privilegiados) |
| **OSINT IOC**           | Georreferenciamento + listas negras (Spamhaus ZEN) |
| **SOC Analyst AI**      | Heurísticas de resposta automática |

### 2. Contra-Medidas Ativas (EDR/RASP)

- **RASP Shield** — Proteção em runtime (bloqueio de `globals()` / builtins perigosos)
- **Network Hex Hunter** — Análise de frames e detecção de padrões de buffer overflow
- **YARA Memory Scan** — Pattern matching em memória volátil
- **DNS Tunneling Detector** — Detecção via entropia de Shannon
- **Anomaly Engine** — Z-Score para detecção de comportamento anômalo (ransomware-like)

### 3. Laboratório Ofensivo

- **Attack Path Mapper** — Lógica estilo BloodHound (DFS) para mapeamento de privilégios
- **Hash Cracker** — Ataque de dicionário contra SHA/MD5

---

## 🚀 Instalação Rápida

### Pré-requisitos

- Docker
- Docker Compose

### Subir o ambiente

```bash
# Entre no diretório do laboratório
cd "landingpage erivelton/sec-analyzers-lab"

# Pare containers anteriores (se houver)
docker-compose down

# Build e suba tudo
docker-compose up -d --build
Acesse a interface
Após a subida dos containers, abra no navegador:
texthttp://localhost:8080
A API estará disponível em:
texthttp://localhost:8000

📁 Estrutura do Projeto
textlandingpage erivelton/
└── sec-analyzers-lab/
    ├── backend/          # API FastAPI
    ├── gui/              # Frontend tático
    ├── waf/              # WAF Engine
    ├── bot/              # Attack Simulator
    ├── sast/             # Análise estática
    ├── dast/             # Análise dinâmica
    ├── cloud/            # Auditoria cloud
    ├── tests/            # Testes
    ├── Dockerfile
    └── docker-compose.yml

⚠️ Aviso Importante
Este laboratório contém ferramentas ofensivas e de análise de segurança.

Use apenas em ambientes controlados e com autorização.

Não utilize contra sistemas de terceiros sem permissão explícita.

👨‍💻 Autor
Erivelton Rocha

Software Engineer & Cybersecurity

Portfólio: eriveltonrochaportifolio1.pages.dev
LinkedIn: eriveltonrocha18


📄 Licença
Este projeto é disponibilizado para fins educacionais e de pesquisa em segurança.
