import json, urllib.request

key = [l.split('api_key: ')[1].strip() for l in open('/home/aqua/.hermes/config.yaml') if 'api_key: fw_' in l][0]
req = urllib.request.Request('https://api.fireworks.ai/inference/v1/models',
                             headers={'Authorization': f'Bearer {key}'})
with urllib.request.urlopen(req, timeout=60) as r:
    data = json.load(r)
for m in data['data']:
    mid = m['id'].lower()
    if 'kimi' in mid or 'glm' in mid:
        print(m['id'])
