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
