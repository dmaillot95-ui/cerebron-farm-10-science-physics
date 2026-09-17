import json, os, pathlib
from hf_gradio import gradio_client

role = os.environ['ROLE']
model = os.environ['MODEL']
focus = os.environ.get('FOCUS','general physics')
mission = pathlib.Path('mission/SCIENCE-PHYSICS-MISSION.md').read_text()
prompt = f'''You are role {role} in CEREBRON Farm 10 Science Physics.
Focus: {focus}
Mission rules:\n{mission}\n
Produce a rigorous physics analysis. Define symbols and units, check dimensions, state assumptions and validity domain, separate established facts from derivations/models/speculation, actively seek falsification, and end with a compact verdict ledger. Do not claim experimental validation unless evidence is provided.'''

out = {'role': role, 'model': model, 'focus': focus, 'success': False}
try:
    client = gradio_client.Client(model)
    result = client.predict(message=prompt, api_name='/chat')
    out['success'] = True
    out['result'] = result
except Exception as e:
    out['error'] = repr(e)

pathlib.Path('results').mkdir(exist_ok=True)
pathlib.Path(f"results/{role}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
print(json.dumps({'role':role,'success':out['success']}))