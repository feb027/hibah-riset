import json, urllib.request, sys

key = [l.split('api_key: ')[1].strip() for l in open('/home/aqua/.hermes/config.yaml') if 'api_key: fw_' in l][0]
candidates = [
    'accounts/fireworks/models/glm-5p3-flash',
    'accounts/fireworks/models/kimi-k2p5',
    'accounts/fireworks/models/kimi-k2p5-turbo',
    'accounts/fireworks/models/kimi-k2-instruct',
]
for model in candidates:
    req = urllib.request.Request(
        'https://api.fireworks.ai/inference/v1/chat/completions',
        data=json.dumps({'model': model, 'messages': [{'role': 'user', 'content': 'reply: OK'}], 'max_tokens': 10}).encode(),
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            out = json.load(r)
        print(model, '->', out['choices'][0]['message']['content'][:30])
    except urllib.error.HTTPError as e:
        print(model, '-> HTTP', e.code)
