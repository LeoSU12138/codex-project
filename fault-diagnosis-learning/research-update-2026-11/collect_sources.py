"""Bounded source refresh; preserve proxy/TLS, never infer success from a URL."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.request
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
CACHE = Path('/tmp/fault-diagnosis-source-refresh')
SOURCES = [
    ('N01', 'tool', 'Captum', 'https://raw.githubusercontent.com/pytorch/captum/master/README.md'),
    ('N02', 'tool', 'Quantus', 'https://raw.githubusercontent.com/understandable-machine-intelligence-lab/Quantus/main/README.md'),
    ('N03', 'author_repository', 'TS2Vec', 'https://raw.githubusercontent.com/zhihanyue/ts2vec/main/README.md'),
    ('N04', 'author_repository', 'PatchTST', 'https://raw.githubusercontent.com/yuqinie98/PatchTST/main/README.md'),
    ('N05', 'author_repository', 'Mamba', 'https://raw.githubusercontent.com/state-spaces/mamba/main/README.md'),
    ('N06', 'author_repository', 'DomainBed', 'https://raw.githubusercontent.com/facebookresearch/DomainBed/main/README.md'),
    ('N07', 'author_repository', 'NeuralOperator', 'https://raw.githubusercontent.com/neuraloperator/neuraloperator/main/README.rst'),
    ('N08', 'author_repository', 'Chronos', 'https://raw.githubusercontent.com/amazon-science/chronos-forecasting/main/README.md'),
    ('C06', 'existing_author_repository', 'CS-SHAP', 'https://raw.githubusercontent.com/ChenQian0618/CS-SHAP/main/README.md'),
    ('C10', 'existing_author_repository', 'Vibration XAI evaluation', 'https://raw.githubusercontent.com/o-mey/xai-vibration-fault-detection/main/README.md'),
    ('S04', 'existing_author_repository', 'UDTL', 'https://raw.githubusercontent.com/ZhaoZhibin/UDTL/master/README.md'),
    ('E01', 'selected_code', 'CS-SHAP transform wrapper', 'https://raw.githubusercontent.com/ChenQian0618/CS-SHAP/main/SHAPs/DomainTransform.py'),
    ('E02', 'selected_code', 'CS-SHAP explanation wrapper', 'https://raw.githubusercontent.com/ChenQian0618/CS-SHAP/main/SHAPs/MultiDomain_SHAP.py'),
    ('E03', 'selected_code', 'DomainBed model selection', 'https://raw.githubusercontent.com/facebookresearch/DomainBed/main/domainbed/model_selection.py'),
    ('B01', 'official_example', 'VAE example', 'https://raw.githubusercontent.com/pytorch/examples/main/vae/README.md'),
    ('B02', 'official_example', 'DCGAN example', 'https://raw.githubusercontent.com/pytorch/examples/main/dcgan/README.md'),
    ('B03', 'author_repository', 'Improved diffusion', 'https://raw.githubusercontent.com/openai/improved-diffusion/main/README.md'),
    ('B04', 'author_repository', 'Temporal Convolutional Networks', 'https://raw.githubusercontent.com/locuslab/TCN/master/README.md'),
    ('B05', 'author_repository', 'Graph Attention Networks', 'https://raw.githubusercontent.com/PetarV-/GAT/master/README.md'),
    ('B06', 'author_repository', 'Physics Informed Neural Networks', 'https://raw.githubusercontent.com/maziarraissi/PINNs/master/README.md'),
    ('Q01', 'database_query', 'Crossref: feature mining and fault diagnosis', 'https://api.crossref.org/works?query=interpretable%20fault%20diagnosis%20feature%20mining&rows=10'),
    ('Q02', 'database_query', 'arXiv: fault diagnosis and explainability', 'https://export.arxiv.org/api/query?search_query=all:%22fault%20diagnosis%22%20AND%20all:explainable&start=0&max_results=10'),
    ('P01', 'candidate_probe', 'Existing systematic review candidate', 'https://doi.org/10.1016/j.ress.2025.111935'),
    ('P02', 'candidate_probe', 'Existing engine valve clearance candidate', 'https://www.mdpi.com/1424-8220/26/11/3565'),
    ('W01', 'workflow_only', 'Scientific Agent Skills provenance', 'https://arxiv.org/abs/2609.00065'),
]

def fetch(item):
    key, kind, title, url = item
    row = dict(id=key, kind=kind, title=title, url=url,
               retrieved_at=datetime.now(timezone.utc).isoformat())
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'FaultDiagnosisLearning-source-audit/1.0'})
        with urllib.request.urlopen(request, timeout=25) as response:
            data = response.read(2_000_001)
            if len(data) > 2_000_000:
                raise ValueError('Source exceeds bounded retrieval size')
            row.update(status='retrieved', http_status=response.status,
                       resolved_url=response.url, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
            (CACHE / (key + '.txt')).write_bytes(data)
    except Exception as error:
        row.update(status='not_retrieved', error=str(error))
    return row

if __name__ == '__main__':
    CACHE.mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(fetch, SOURCES))
    output = {'scope': 'Targeted repository/documentation refresh plus bounded database attempts; not a systematic review',
              'full_papers_assessed': 0, 'model_experiments_run': False, 'sources': rows}
    (ROOT / 'SOURCE_RETRIEVAL.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    for row in rows:
        print(row['id'], row['status'], row.get('bytes', row.get('error')))
