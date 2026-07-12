import json
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Carregar variáveis do .env
load_dotenv()

# Inicializa o cliente oficial da Hugging Face
# O cliente já gere a autenticação pelo api_key
client = InferenceClient(api_key=os.getenv("HF_API_TOKEN"))

def load_profile(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def generate_file_content(file_info, language):
    # Definimos o ID do modelo que pretendemos usar
    model_id = "WizardLM/WizardCoder-15B-V1.0"
    
    # Construção do prompt seguindo a estrutura de instrução do modelo
    prompt = f"### Instruction:\nEscreve apenas código {language} para um ficheiro chamado {file_info['name']}. {file_info['description']}\n\n### Response:\n"
    
    # Chamada à API de inferência
    response = client.text_generation(
        model=model_id,
        prompt=prompt,
        max_new_tokens=200,
        temperature=0.2
    )
    return response

# 1. Carregar o perfil
perfil = load_profile('profile.json')
print(f"A iniciar geração para o projeto: {perfil['project_name']}")

# 2. Criar a pasta do repositório local
repo_path = f"./{perfil['project_name']}"
os.makedirs(repo_path, exist_ok=True)

# 3. Gerar os ficheiros com o WizardCoder
for file in perfil['files']:
    print(f"A pedir à IA para gerar {file['name']}...")
    content = generate_file_content(file, perfil['language'])
    
    if content:
        with open(os.path.join(repo_path, file['name']), 'w') as f:
            f.write(content)
        print(f"Ficheiro {file['name']} guardado com sucesso!")