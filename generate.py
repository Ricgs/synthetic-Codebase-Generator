import os

def generate_file_content(file_info, original_content, language, client):
    """Generates synthetic file content by sanitizing the original code."""
    print(f"-> Asking the AI to rewrite and sanitize: {file_info['name']}...")
    
    message = (
        f"Act as a senior software engineer. Write exclusively the functional source code in {language} "
        f"for the file '{file_info['name']}'. Do not add any explanations in text, Markdown or additional code blocks. "
        f"The code must be architecturally identical to the original code below, maintaining the exact same structure, "
        f"classes, dependencies, and design patterns, but you MUST replace all proprietary business logic, "
        f"confidential information, and internal secrets with synthetic equivalents.\n\n"
        f"--- ORIGINAL CODE ---\n{original_content}\n"
    )
    
    messages = [{"role": "user", "content": message}]
    
    response = client.chat.completions.create(
        model="qwen2.5-coder:7b",
        messages=messages,
        max_tokens=2000, # Aumentado para suportar ficheiros inteiros
        temperature=0.1  # Reduzido de 0.2 para forçar maior rigor estrutural
    )
    return response.choices[0].message.content

def write_workflow_file(repo_path):
    """Injects automatically the CI/CD workflow to test the synthetic repository."""
    workflow_dir = os.path.join(repo_path, ".github/workflows")
    os.makedirs(workflow_dir, exist_ok=True)
    
    ci_content = """name: Synthetic Repository CI/CD

on: [push, pull_request]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    - name: Install Synthetic Dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

    - name: Run Unit Tests
      env:
        PYTHONPATH: .
      run: |
        pytest
"""
    with open(os.path.join(workflow_dir, "ci.yml"), "w", encoding="utf-8") as f:
        f.write(ci_content)
    print("Workflow CI/CD (.github/workflows/ci.yml) injected successfully!")

# A função agora recebe 'source_repo_path' para poder ler o código original
def generate_synthetic_repo(profile, source_repo_path, repo_path, client):
    """Generates a synthetic repository based on direct code sanitization."""
    os.makedirs(repo_path, exist_ok=True)

    if profile.get('dependencies_file') and profile.get('dependencies'):
        dep_file_path = os.path.join(repo_path, profile['dependencies_file'])
        with open(dep_file_path, "w", encoding='utf-8') as f:
            f.write(profile['dependencies'])
        print(f"Dependency file ({profile['dependencies_file']}) created successfully!")

    for file in profile['files']:
        rel_path = file['name']
        full_file_path = os.path.join(repo_path, rel_path)
        orig_file_path = os.path.join(source_repo_path, rel_path)
        
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        
        if os.path.exists(orig_file_path):
            with open(orig_file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
                
            # Passa o conteúdo original diretamente para o modelo
            content = generate_file_content(file, original_content, profile.get('language', 'python'), client)
            
            if content:
                clean_content = content.replace("```python", "").replace("```", "").strip()
                with open(full_file_path, 'w', encoding='utf-8') as f:
                    f.write(clean_content)
                print(f"✔ Saved: {rel_path}")
        else:
            print(f"Warning: Original file not found at {orig_file_path} - Generation skipped.")

    write_workflow_file(repo_path)