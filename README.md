🛡️ XDR Neo-Platform | Enterprise Security Lab
Plataforma unificada de Extended Detection and Response (XDR) e Inteligência Cibernética Operacional



 [blocked]
 [blocked]
Laboratório de segurança ofensiva e defensiva com algoritmos reais de detecção, resposta e inteligência cibernética.

Ambiente completamente isolado via microserviços orquestrados por Docker Compose.

🎯 Visão Geral
A XDR Neo-Platform não é um simulador superficial.

A maioria das funcionalidades da interface aciona algoritmos reais de análise estatística, pattern matching e engenharia reversa implementados no núcleo da API.
Foi desenvolvida com o objetivo de simular um ambiente de SOC completo, unindo capacidades de Blue Team e Red Team.
Principais Capacidades

































































CapacidadeDescrição TécnicaTipoExtended Detection & ResponseCorrelação de eventos multi-fonteBlue TeamSAST (Static Analysis)Análise de código via ASTBlue TeamDAST (Dynamic Analysis)Fuzzing web + detecção de LFIBlue TeamCloud / IaC AuditValidação de containers e YAMLBlue TeamOSINT + IOC CorrelationGeorreferenciamento + listas negrasBlue TeamRASP (Runtime Protection)Proteção em runtimeBlue TeamDNS Tunneling DetectionDetecção via Entropia de ShannonBlue TeamAnomaly DetectionZ-Score para comportamento anômaloBlue TeamAttack Path MapperMapeamento de privilégios (BloodHound)Red TeamHash CrackerAtaque de dicionário (SHA/MD5)Red TeamWAF + Attack SimulatorProteção web + simulação de ataquesDual

🏗️ Arquitetura
textFrontend Tático (HTML/CSS/JS) → Porta 8080
              ↓
Backend SIEM (FastAPI) → Porta 8000
     ├── SAST
     ├── DAST
     ├── Cloud Audit
     ├── WAF Engine
     └── Attack Simulator
Serviços Docker













































ServiçoPortaFunçãobackend8000API principal + SIEMxdr-gui8080Interface webwaf-engine8081Web Application Firewallsast-Análise estáticadast-Testes dinâmicoscloud-Auditoria Cloud/IaCattack-simulator-Simulador de ataques

🛠️ Módulos Principais
1. Análise de Inteligência (SIEM)

Painel de telemetria em tempo real
SAST com AST
DAST com fuzzing
Auditoria Cloud/IaC
Correlação de IOCs via OSINT

2. Contra-Medidas Ativas (EDR/RASP)

RASP Shield
Network Hex Hunter
YARA Memory Scan
DNS Tunneling Detector
Anomaly Engine (Z-Score)

3. Laboratório Ofensivo

Attack Path Mapper (estilo BloodHound)
Hash Cracker


🚀 Como Executar
Pré-requisitos

Docker
Docker Compose

Comandos
Bashgit clone https://github.com/EriveltonRocha77/-XDR-Platform-Enterprise-Security-Lab-.git
cd "-XDR-Platform-Enterprise-Security-Lab-/landingpage erivelton/sec-analyzers-lab"
docker-compose down
docker-compose up -d --build
Acessos

Interface Web: http://localhost:8080
API Backend: http://localhost:8000
WAF: http://localhost:8081


🧰 Stack Tecnológica

Backend: Python + FastAPI
Análise: AST, YARA, Z-Score, Shannon Entropy
Frontend: HTML, CSS, JavaScript
Infraestrutura: Docker + Docker Compose
Segurança: WAF, RASP, OSINT


🎓 Aprendizados

Arquitetura de microserviços orientada a segurança
Correlação de eventos (SIEM)
Detecção de anomalias estatísticas
Proteção em runtime (RASP)
Orquestração com Docker Compose


👨‍💻 Autor
Erivelton da Rocha Silva

Estudante de Engenharia de Software e Segurança da Informação

Sertãozinho / SP - Brasil

LinkedIn: linkedin.com/in/eriveltonrocha18
Portfólio: eriveltonrochaportifolio1.pages.dev
GitHub: github.com/EriveltonRocha77
Email: eriveltoncurriculo@gmail.com


📄 Licença
Este projeto está sob a licença MIT.
