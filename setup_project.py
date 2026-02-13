import os

# Create ALL directories (safe - no errors if exist)
folders = [
    'data/raw', 'data/clean', 
    'notebooks', 'src', 
    'images', 'reports'
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"✅ {folder}/")

print("\n🎉 PROJECT STRUCTURE READY!")
print("📁 Current structure:")
for root, dirs, files in os.walk('.'):
    level = root.replace('.', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 2 * (level + 1)
    for d in dirs[:3]:  # First 3 dirs
        print(f"{subindent}{d}/")
    for f in files[:3]:  # First 3 files
        print(f"{subindent}{f}")
    break
