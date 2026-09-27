import os
import json

def generate_file_description(file_path, content, client):
    """Asks the LLM to generate a description for a file."""
    print(f"-> Generating description for: {file_path}...")
    message = (
        f"A '{file_path}'. "
        f"Write a technical and concise description (maximum 3 sentences) that explains its structure, "
        f"classes, main methods and dependencies. Do not copy the original code. "
        f"This description will be used to recreate a functionally similar file.\n\n"
        f"Original code:\n```\n{content}\n```"
    )
    
    messages = [{"role": "user", "content": message}]
    response = client.chat.completions.create(
        model="qwen2.5-coder:7b", # Define o modelo local a usar
        messages=messages,
        max_tokens=250,
        temperature=0.1
    )
    # Nova extração do conteúdo da resposta
    return response.choices[0].message.content.strip()

def profile_repository(source_repo_path, client, output_profile_path="profile.json"):
    """Profiles the repository and generates a JSON profile."""
    ignore_dirs = {'.git', '__pycache__', 'venv', '.venv', 'node_modules', '.github'}
    valid_extensions = {'.py', '.js', '.ts', '.md', '.txt'}
    
    project_name = os.path.basename(os.path.normpath(source_repo_path))
    if not project_name:
        project_name = "default-project"
        
    common_dependency_files = [
        'requirements.txt', 'pyproject.toml', 'Pipfile', # Python
        'package.json', 'yarn.lock',                     # Node.js
        'pom.xml', 'build.gradle',                       # Java
        'go.mod',                                        # Go
        'Cargo.toml'                                     # Rust
    ]
    
    profile = {
        "project_name": "synthetic-" + os.path.basename(os.path.normpath(source_repo_path)),
        "language": "Infer from files", 
        "dependencies_file": None,
        "dependencies": [],
        "files": []
    }
    
    found_dep_file = None
    for dep_file in common_dependency_files:
        req_path = os.path.join(source_repo_path, dep_file)
        if os.path.exists(req_path):
            found_dep_file = dep_file
            break
            
    if found_dep_file:
        profile["dependencies_file"] = found_dep_file
        req_path = os.path.join(source_repo_path, found_dep_file)
        with open(req_path, 'r', encoding='utf-8') as f:
            profile["dependencies"] = f.read()
        print(f"Dependency file found: {found_dep_file}")
    else:
        print("Warning: No standard dependency file was found.")
    
    for root, dirs, files in os.walk(source_repo_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            if found_dep_file and file == found_dep_file:
                continue
                
            if not any(file.endswith(ext) for ext in valid_extensions):
                continue
                
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, source_repo_path)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if len(content) > 15000:
                    content = content[:15000] + "\n...[Truncated]..."
                    
                description = generate_file_description(rel_path, content, client)
                profile["files"].append({
                    "name": rel_path,
                    "description": description
                })
            except Exception as e:
                print(f"Error processing {rel_path}: {e}")
                
    with open(output_profile_path, 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    print(f"Profile saved successfully to {output_profile_path}")
    return profile