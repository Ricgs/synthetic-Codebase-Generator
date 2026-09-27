import os
import json

def profile_repository(source_repo_path, output_profile_path="profile.json"):
    """Profiles the repository mapping the file tree and capturing dependencies."""
    print(f"\n=== FASE 1: Mapping repository structure for '{source_repo_path}' ===")
    
    ignore_dirs = {'.git', '__pycache__', 'venv', '.venv', 'node_modules', '.github'}
    valid_extensions = {'.py', '.js', '.ts', '.md', '.txt', '.json', '.yml', '.yaml'}
    
    project_name = os.path.basename(os.path.normpath(source_repo_path))
    if not project_name:
        project_name = "default-project"
        
    common_dependency_files = [
        'requirements.txt', 'pyproject.toml', 'Pipfile', 
        'package.json', 'yarn.lock',                     
        'pom.xml', 'build.gradle',                       
        'go.mod',                                        
        'Cargo.toml'                                     
    ]
    
    profile = {
        "project_name": "synthetic-" + os.path.basename(os.path.normpath(source_repo_path)),
        "language": "Infer from files", 
        "dependencies_file": None,
        "dependencies": "",
        "files": []
    }
    
    # 1. Identificar e extrair o ficheiro de dependências principal
    found_dep_file = None
    for dep_file in common_dependency_files:
        req_path = os.path.join(source_repo_path, dep_file)
        if os.path.exists(req_path):
            found_dep_file = dep_file
            break
            
    if found_dep_file:
        profile["dependencies_file"] = found_dep_file
        with open(os.path.join(source_repo_path, found_dep_file), 'r', encoding='utf-8') as f:
            profile["dependencies"] = f.read()
        print(f"Dependency file found: {found_dep_file}")
    else:
        print("Warning: No standard dependency file was found.")
    
    # 2. Mapear a árvore de diretórios e os ficheiros de código
    for root, dirs, files in os.walk(source_repo_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            # Ignora o ficheiro de dependências, pois já foi guardado na raiz do perfil
            if found_dep_file and file == found_dep_file:
                continue
                
            if not any(file.endswith(ext) for ext in valid_extensions):
                continue
                
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, source_repo_path)
            
            print(f"-> Mapping file: {rel_path}")
            # Guardamos apenas o caminho. A leitura do conteúdo fica para a Fase 2.
            profile["files"].append({
                "name": rel_path
            })
                
    with open(output_profile_path, 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
        
    print(f"Profile structure saved successfully to {output_profile_path}")
    return profile