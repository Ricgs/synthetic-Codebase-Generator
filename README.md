# 🧪 CI/CD Synthetic Workload Generator

Este projeto é um componente da dissertação de Mestrado. Consiste num gerador automatizado de cargas de trabalho sintéticas (workloads) utilizando Modelos de Linguagem de Grande Escala (LLMs).

## 📌 Objetivo Metodológico
Gerar repositórios de código funcionais, com infraestrutura CI/CD (GitHub Actions), baseados em perfis anonimizados. Isto permite exercitar e validar ferramentas de análise estática de segurança (SAST) em ambientes de Sandbox, sem expor propriedade intelectual real.

## 🚀 Como Executar

NOTA: O modelo atual do gerador recorre a LLMs locais, com recurso do Ollama.

1. Clonar o repositório.

2. Criar ambiente virtual e instalar dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Executar o gerador:
   ```bash
   python main.py
   ```
