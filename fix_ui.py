with open('enhance_ui.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
# Replace the last line (incomplete) with closing triple quotes
if lines:
    lines[-1] = "'''\n"
with open('enhance_ui.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Fixed enhance_ui.py")
