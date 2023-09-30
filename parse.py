import subprocess
import json
from pathlib import Path

directory = "./data/Themes_2&4_Visualization_and_Summarization/Specific_Encounter_Examples/"

p = Path(directory)
files = list(p.glob('**/*.xml'))

for path_to_file in files:
    print(path_to_file)
    # if node isn't on your path, the first arg should instead be a path to the node bin
    cmd_list = ['node', 'parseClinicalXml.js', path_to_file]

    p = subprocess.Popen(cmd_list, stdout=subprocess.PIPE,
        stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    result, error = p.communicate()
    p.stdin.close()

    if p.returncode != 0:
        print(error)
        raise ValueError("Failed to parse clinical XML at %s" % \
            path_to_file)

    parsed_data = json.loads(result)
    #Save the json data into path_to_file with json extension
    with open(path_to_file.with_suffix('.json'), 'w') as f:
        json.dump(parsed_data, f)
