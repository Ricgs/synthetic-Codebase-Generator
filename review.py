import os

def review_synthetic_code(original_content, synthetic_content, client):
    """Compares the original and synthetic code to validate the quality of generation."""
    message = (
        "Act as a code auditor. Compare the following original code with the generated synthetic version. "
        "Verify if the synthetic version maintains a similar structure (classes, dependencies, cyclomatic complexity) "
        "sufficient to realistically exercise CI/CD pipelines (linters, static tests, SAST). "
        "The synthetic code MUST NOT contain any confidential business logic from the original. "
        "Respond with 'APPROVED' or 'NOT APPROVED', followed by bullet points with the justification.\n\n"
        f"--- ORIGINAL ---\n{original_content}\n\n"
        f"--- SINTÉTICO ---\n{synthetic_content}"
    )
    
    messages = [{"role": "user", "content": message}]
    response = client.chat.completions.create(
        model="qwen2.5-coder:7b",
        messages=messages,
        max_tokens=300,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def review_repository(source_repo_path, synthetic_repo_path, profile, client):
    """Reviews the synthetic repository against the original and saves a report."""
    print("\n=== Initiating Automatic Review Phase ===")
    
    report_path = "review_report.md"
    
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write(f"# Synthetic Code Review Report\n")
        report_file.write(f"**Source Repository:** {source_repo_path}\n\n")
        
        for file_info in profile['files']:
            rel_path = file_info['name']
            orig_path = os.path.join(source_repo_path, rel_path)
            synth_path = os.path.join(synthetic_repo_path, rel_path)
            
            if os.path.exists(orig_path) and os.path.exists(synth_path):
                print(f"-> Reviewing: {rel_path}")
                
                with open(orig_path, 'r', encoding='utf-8') as f:
                    orig_content = f.read()
                with open(synth_path, 'r', encoding='utf-8') as f:
                    synth_content = f.read()
                    
                result = review_synthetic_code(orig_content, synth_content, client)
                
                output_text = f"\n### File: `{rel_path}`\n{result}\n{'-'*40}"
                
                print(output_text)
                report_file.write(output_text + "\n")
            else:
                msg = f"Warning: Original or synthetic file not found for {rel_path} - Review skipped."
                print(msg)
                report_file.write(f"\n### File: `{rel_path}`\n- {msg}\n")
                
    print(f"\n✔ Review phase completed. Full report saved to '{report_path}'.")
