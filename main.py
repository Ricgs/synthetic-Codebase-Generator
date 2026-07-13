import json
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
token = os.getenv("HF_API_TOKEN")

# Inicializa o cliente com o modelo LLM Coder padrão da API Serverless
client = InferenceClient(model="Qwen/Qwen2.5-Coder-7B-Instruct", token=token)

def load_profile(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def generate_file_content(file_info, language):
    print(f"-> A pedir à IA para gerar: {file_info['name']}...")
    
    # Customização do prompt para instruir o modelo a focar-se apenas no código puro
    mensagem = (
        f"Age como um engenheiro de software sénior. Escreve exclusivamente o código fonte funcional em {language} "
        f"para o ficheiro '{file_info['name']}'. Não adiciones nenhuma explicação em texto, Markdown ou blocos de código adicionais. "
        f"O código deve cumprir este requisito: {file_info['description']}"
    )
    
    messages = [{"role": "user", "content": mensagem}]
    
    response = client.chat_completion(
        messages=messages,
        max_tokens=700,
        temperature=0.2
    )
    return response.choices[0].message.content

def write_workflow_file(repo_path):
    """Injeta automaticamente o workflow de CI/CD para testar o repositório sintético."""
    workflow_dir = os.path.join(repo_path, ".github/workflows")
    os.makedirs(workflow_dir, exist_ok=True)
    
    ci_content = """name: Pipeline de Teste Sintetizado

on: [push, pull_request]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout do Código Sintético
      uses: actions/checkout@v4

    - name: Configurar Ambiente Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    - name: Instalar Dependências Sintéticas
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

    - name: Executar Testes Unitários
      env:
        PYTHONPATH: .
      run: |
        pytest
"""
    with open(os.path.join(workflow_dir, "ci.yml"), "w") as f:
        f.write(ci_content)
    print("Workflow CI/CD (.github/workflows/ci.yml) injetado com sucesso!")

# --- Fluxo de Execução Principal ---
perfil = load_profile('profile.json')
repo_path = f"./{perfil['project_name']}"
os.makedirs(repo_path, exist_ok=True)

print(f"=== A iniciar geração do Workload para: {perfil['project_name']} ===")

# 1. Gerar ficheiro de dependências automaticamente
if 'dependencies_file' in perfil:
    dep_file_path = os.path.join(repo_path, perfil['dependencies_file'])
    with open(dep_file_path, "w") as f:
        f.write("\n".join(perfil['dependencies']))
    print(f"Ficheiro de dependências ({perfil['dependencies_file']}) criado com sucesso!")

# 2. Gerar recursivamente os ficheiros de código através do LLM
for file in perfil['files']:
    # Extrai o caminho completo e garante que as subpastas existem antes de gravar
    full_file_path = os.path.join(repo_path, file['name'])
    os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
    
    content = generate_file_content(file, perfil['language'])
    
    if content:
        # Limpa eventuais resíduos de formatação markdown ``` que o modelo possa retornar
        clean_content = content.replace("```python", "").replace("```", "").strip()
        with open(full_file_path, 'w') as f:
            f.write(clean_content)
        print(f"✔ Guardado em: {file['name']}")

# 3. Injetar a infraestrutura de CI/CD para o ambiente sandbox
write_workflow_file(repo_path)

print(f"\n=== Sucesso: Repositório sintético estruturado em '{repo_path}' ===")