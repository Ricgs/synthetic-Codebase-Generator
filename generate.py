import os

def generate_file_content(file_info, language, client):
    """Generates synthetic file content based on the profile description."""
    print(f"-> Asking the AI to generate: {file_info['name']}...")
    
    message = (
        f"Act as a senior software engineer. Write exclusively the functional source code in {language} "
        f"for the file '{file_info['name']}'. Do not add any explanations in text, Markdown or additional code blocks. "
        f"The code must fulfill this requirement: {file_info['description']}"
    )
    
    messages = [{"role": "user", "content": message}]
    
    response = client.chat.completions.create(
        model="qwen2.5-coder:7b",
        messages=messages,
        max_tokens=700,
        temperature=0.2
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

def generate_synthetic_repo(profile, repo_path, client):
    """Generates a synthetic repository based on the profile."""
    os.makedirs(repo_path, exist_ok=True)

    if profile.get('dependencies_file') and profile.get('dependencies'):
        dep_file_path = os.path.join(repo_path, profile['dependencies_file'])
        with open(dep_file_path, "w", encoding='utf-8') as f:
            f.write(profile['dependencies'])
        print(f"Dependency file ({profile['dependencies_file']}) created successfully!")

    for file in profile['files']:
        full_file_path = os.path.join(repo_path, file['name'])
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        
        content = generate_file_content(file, profile['language'], client)
        
        if content:
            clean_content = content.replace("```python", "").replace("```", "").strip()
            with open(full_file_path, 'w', encoding='utf-8') as f:
                f.write(clean_content)
            print(f"✔ Saved: {file['name']}")

    write_workflow_file(repo_path)