import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from profiling import profile_repository
from generate import generate_synthetic_repo
from review import review_repository

def main():
    load_dotenv()
    token = os.getenv("HF_API_TOKEN")
    
    if not token:
        print("Error: No HF_API_TOKEN found in environment variables. Please set it in the .env file.")
        return

    client = OpenAI(
        base_url='http://localhost:11434/v1',
        api_key='ollama' # Chave obrigatória para o SDK, mas ignorada localmente
    )
    
    source_repo = "fastapi-realworld-example-app"
    profile_file = "profile.json"
    
    os.makedirs(source_repo, exist_ok=True)
    
    # --- FASE 1: PROFILING ---
    print(f"\n=== FASE 1: Profile extraction for '{source_repo}' ===")
    if os.listdir(source_repo): 
        perfil = profile_repository(source_repo, client, profile_file)
    else:
        print(f"The repository '{source_repo}' is empty. Add files there or use the Flask/HTTPie.")
        # Fallback to use the existing profile.json (the one from the calculator) to avoid breaking the execution
        if os.path.exists(profile_file):
            print("Using the existing local profile.json as a fallback...")
            with open(profile_file, 'r', encoding='utf-8') as f:
                perfil = json.load(f)
        else:
            print("No repository and no profile.json. Aborting.")
            return

    # --- FASE 2: GERAÇÃO ---
    synthetic_repo = f"./{perfil['project_name']}"
    print(f"\n=== FASE 2: Synthetic Repository Generation for '{synthetic_repo}' ===")
    generate_synthetic_repo(perfil, synthetic_repo, client)
    print(f"\nSuccess: Synthetic repository generated for '{synthetic_repo}'")

    # --- FASE 3: REVISÃO ---
    if os.listdir(source_repo):
        review_repository(source_repo, synthetic_repo, perfil, client)
    else:
        print("\n=== FASE 3: Review ignored (no original base code available for comparison) ===")

if __name__ == "__main__":
    main()