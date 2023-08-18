import subprocess

path = "src/asm/helloworld.asm"

to_obj = f"nasm -f win32 {path}"
result = subprocess.call(to_obj)
if(result != 0): 
    exit(69)
    
path = path.replace('.asm', '.obj')
exe = path.replace('.obj', '.exe')
link = f"gcc {path} -o {exe}".split(' ')
result = subprocess.call(link)
if(result != 0): 
    exit(69)

subprocess.call([exe])