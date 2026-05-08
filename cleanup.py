with open('omnisec_engine.py', 'r') as f:
    lines = f.readlines()

clean_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # If this is a logger.error line with incorrect indentation
    if line.startswith('            ') and 'logger.error(f"[' in line and 'target_ip' in line:
        # Skip this line and the next one if it's 'return False'
        i += 1
        if i < len(lines) and lines[i].strip() == 'return False':
            i += 1
        continue
    clean_lines.append(line)
    i += 1

with open('omnisec_engine.py', 'w') as f:
    f.writelines(clean_lines)

print('Cleaned up incorrect logger.error lines')