# 🧪 CI/CD Synthetic Workload Generator

Este projeto é um componente da dissertação de Mestrado focada em segurança e integração contínua (CI/CD). Consiste num gerador automatizado de cargas de trabalho sintéticas (workloads) utilizando Modelos de Linguagem de Grande Escala (LLMs).

## 📌 Objetivo Metodológico
Gerar repositórios de código funcionais, com testes unitários e infraestrutura CI/CD (GitHub Actions), baseados em perfis anonimizados (`profile.json`). Isto permite exercitar e validar ferramentas de análise estática de segurança (SAST) em ambientes de Sandbox, sem expor propriedade intelectual real.

## ⚙️ Arquitetura e Modelos
Atualmente, o motor utiliza a **Hugging Face Serverless Inference API** com o modelo `Qwen/Qwen2.5-Coder-7B-Instruct` via a interface de *Chat Completions*, permitindo uma geração rápida e estruturada de infraestruturas agnósticas de linguagem.

## 🚀 Como Executar

1. Clonar o repositório.

2. Criar ambiente virtual e instalar dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configurar a variável de ambiente no ficheiro .env:
   ```bash
   HF_API_TOKEN=teu_token_aqui
   ```
4. Executar o gerador:
   ```bash
   python main.py
   ```