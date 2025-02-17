import json
import re

def parse_markdown_to_json(md_file, json_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []
    current_instruction = None
    current_output = []

    for line in lines:
        # Match for # ## and ###
        header_match = re.match(r'^(#{1,3})\s+(.+)', line.strip())
        
        if header_match:
            if current_instruction:
                data.append({"instruction": current_instruction, "output": "\n".join(current_output).strip()})
            
            current_instruction = header_match.group(2).strip()
            current_output = []
        
        else:
            if current_instruction:
                current_output.append(line.strip())

    if current_instruction:
        data.append({"instruction": current_instruction, "output": "\n".join(current_output).strip()})

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

parse_markdown_to_json("src/input.md", "output.json")
