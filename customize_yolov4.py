from os import path, getcwd
import json

CONFIG_FILE = "yolov4-custom.cfg"

num_classes = sum(1 for line in open(path.join(getcwd(), "classes.txt")))
num_pairs_filterclassses = 0
if CONFIG_FILE == "yolov4-tiny-custom.cfg":
    num_pairs_filterclassses = 2
elif CONFIG_FILE == "yolov4-custom.cfg":
    num_pairs_filterclassses = 3

# Good to stay within Google Colabs memory limits, change if needed
# add other configuration that you would like automatically change
#   Example: subdivisions, greater values uses less memory but is slower
max_batches = num_classes * 2000
net_config = {
    'width': {'value': "416", 'read': False},
    'height': {'value': "416", 'read': False},
    'max_batches': {'value': str(max_batches), 'read': False},
    'steps': {
        'value': '{0}, {1}'.format(
            int(max_batches * 0.8),
            int(max_batches * 0.9)),
        'read': False,
        },
    }
all_ready = lambda config: all([config[key]['read'] for key in config])
net_params = list(net_config.keys())

print("Configuration to change")
print(json.dumps(net_config, sort_keys=True, indent=4))

lines = []

with open(path.join(getcwd(), CONFIG_FILE), "r") as f:
    lines = [line.strip() for line in f.readlines()]

# Edit lines in our copy
# First from top bottom
for idx, line in enumerate(lines):
    if line == "" or line.startswith("#"):
        continue
    elif all_ready(net_config):
        break
    elif not line.startswith('['):
        param = line.split('=')[0].strip()
        if param in net_params:
            net_config[param]['read'] = True
            lines[idx] = param + "=" + net_config[param]['value']

# Reconfigure the network to use the correct amount of classes
model_config = {
    'classes': str(num_classes),
    'filters': str((num_classes + 5) * 3),
    }
print(json.dumps(model_config, sort_keys=True, indent=4))

# Edit lines in our copy
# From bottom to top
params_counter = 0
last_tag = ""
for idx_1 in range(len(lines), 0, -1):
    idx = idx_1 - 1
    line = lines[idx]
    #print(idx, line)
    if line == "" or line.startswith("#"):
        continue
    elif params_counter >= num_pairs_filterclassses:
        break
    elif line.startswith('['):
        last_tag = line[1:-1]
        continue
    elif not line.startswith('['):
        param = line.split('=')[0].strip()
        if param == "classes":
            lines[idx] = f"{param}={model_config[param]}"
        elif param == "filters" and last_tag == "yolo":
            lines[idx] = f"{param}={model_config[param]}"
            params_counter += 1

output_file = "my-" + CONFIG_FILE[:-11] + ".cfg"
with open(output_file, "w") as f:
    f.write("\n".join(lines) + "\n")

