import io
import yaml

try:
    fsine = input("Enter carrier frequency (Hz) [default = 100]:")
    fsine = int(fsine)
except ValueError:
    fsine = 100
try:
    fsamp = input("Enter sampling frequency (Hz) [default = 44100]:")
    fsamp = int(fsamp)
except ValueError:
    fsamp = 44100
try:
    t_sec = input("Enter approximage length (s) [default = 10]:")
    t_sec = int(t_sec)
except ValueError:
    t_sec = 10

filename = input("Input wav file name (saved in /tmp/) [default = weathertone]:")
if filename == '':
    filename = "weathertone"

data = {
'fsine': fsine,
'fsamp': fsamp,
't_sec': t_sec,
'filename': str(filename)
}

with io.open('wavecfg.yaml', 'w', encoding='utf8') as outfile:
    yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)
