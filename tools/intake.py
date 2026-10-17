#!/usr/bin/env python3
"""Resumable, local orchestration of Bootdisk's existing component CLIs."""
from __future__ import annotations
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

SCHEMA = 'bootdisk-intake-run-1'
SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')


class IntakeError(Exception):
    pass


def require(ok, message):
    if not ok:
        raise IntakeError(message)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def tree(root):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), f'Not a plain directory: {root}')
    result = {}
    for p in sorted(root.rglob('*')):
        require(not p.is_symlink(), f'Symlink not allowed: {p}')
        if p.is_file():
            result[p.relative_to(root).as_posix()] = digest(p)
        else:
            require(p.is_dir(), f'Unsupported file type: {p}')
    return result


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    path = Path(path)
    tmp = path.with_name(path.name + '.tmp')
    require(not tmp.is_symlink() and not path.is_symlink(), 'Unsafe state path')
    tmp.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    os.replace(tmp, path)


def overlap(a, b):
    return a == b or a in b.parents or b in a.parents


def pin_repo(path):
    # Pin tracked and nonignored local files, including uncommitted tool modules.
    files = subprocess.check_output(['git', '-C', str(path), 'ls-files', '--cached', '--others', '--exclude-standard', '-z']).decode().split('\0')
    require(any(files), f'No tracked toolchain files: {path}')
    result = {}
    for name in files:
        if not name:
            continue
        p = path / name
        require(p.is_file() and not p.is_symlink(), f'Missing/unsafe tracked file: {p}')
        result[name] = digest(p)
    return {'head': subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD']).decode().strip(),
            'files': result}


def load_plan(config, workspace):
    config = Path(config).resolve()
    plan = read(config)
    require(plan.get('schema') == SCHEMA, 'Unsupported intake configuration')
    def path(value):
        return (config.parent / value).resolve()
    repos = {k: path(plan['repositories'][k]) for k in ('ingest', 'catalog', 'publish', 'web')}
    inputs = list(repos.values())
    media = plan.get('media', [])
    require(isinstance(media, list) and media, 'At least one medium is required')
    seen = set()
    normalized = []
    for item in media:
        mid = item.get('id', '')
        require(SLUG.fullmatch(mid) and mid not in seen, 'Invalid/duplicate medium id')
        seen.add(mid)
        require(item.get('profile') in ('dtx', 'dtx-workshop'), 'Choose a qualified dtx or dtx-workshop profile')
        require(isinstance(item.get('label'), str) and item['label'].strip(), 'Missing CD label')
        require(bool(item.get('source_root')) != bool(item.get('iso')), 'Choose source_root OR iso')
        m = dict(item)
        key = 'source_root' if item.get('source_root') else 'iso'
        m[key] = str(path(item[key]));inputs.append(Path(m[key]))
        normalized.append(m)
    baseline = path(plan['baseline']) if plan.get('baseline') else None
    if baseline:
        inputs.append(baseline)
    collections = path(plan['collections']) if plan.get('collections') else None
    if collections:
        inputs.append(collections)
    seven = path(plan['seven_zip']) if plan.get('seven_zip') else None
    require(seven or all('source_root' in m for m in normalized), 'ISO input requires an explicit seven_zip executable')
    if seven:
        inputs.append(seven)
    for p in inputs:
        require(p.exists() and not overlap(workspace, p), f'Workspace must be separate from input: {p}')
    fingerprints = {'repositories': {k: pin_repo(p) for k, p in repos.items()},
                    'runner': digest(Path(__file__)), 'python': sys.version,
                    'inputs': {str(p): tree(p) if p.is_dir() and p not in repos.values() else digest(p)
                               for p in inputs if p not in repos.values()}}
    return {'config': plan, 'repositories': {k: str(v) for k, v in repos.items()},
            'media': normalized, 'baseline': str(baseline) if baseline else None,
            'seven_zip': str(seven) if seven else None,
            'collections': str(collections) if collections else None, 'fingerprints': fingerprints}


class Run:
    def __init__(self, root, plan, stop_after=None):
        self.root, self.plan, self.stop_after = Path(root), plan, stop_after
        self.lock = None
        self.completed = []

    def __enter__(self):
        require(not self.root.is_symlink(), 'Workspace cannot be a symlink')
        self.root.mkdir(parents=True, exist_ok=True)
        marker = self.root / 'run.json'
        require(marker.exists() or not any(self.root.iterdir()), 'Refusing an unowned workspace')
        lock_path = self.root / '.lock'
        require(not lock_path.is_symlink(), 'Unsafe lock path')
        self.lock = lock_path.open('a')
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            if marker.exists():
                require(read(marker) == self.plan, 'Inputs/configuration/toolchain changed: use a new workspace')
            else:
                write(marker, self.plan)
        except BaseException:
            self.lock.close()
            raise
        return self

    def __exit__(self, *args):
        self.lock.close()

    def stage(self, name, action):
        require(re.fullmatch(r'[a-z0-9-]+', name), 'Unsafe stage name')
        final = self.root / name
        if final.exists() or final.is_symlink():
            actual = tree(final)
            receipt = read(final / '_receipt.json')
            actual.pop('_receipt.json', None)
            require(actual == receipt['files'], f'Completed stage changed: {name}; refusing overwrite')
            print(f'Gjenbruker {name}', flush=True)
        else:
            partial = self.root / ('.' + name + '.partial')
            require(not partial.is_symlink(), 'Unsafe partial stage')
            if partial.exists():
                shutil.rmtree(partial)
            partial.mkdir()
            print(f'Kjører {name}', flush=True)
            action(partial)
            write(partial / '_receipt.json', {'files': tree(partial)})
            os.rename(partial, final)
        self.completed.append(name)
        if self.stop_after == name:
            raise KeyboardInterrupt(f'Planned stop after {name}')
        return final


def union_store(sources, output):
    output.mkdir(parents=True)
    for source in sources:
        for rel, sha in tree(source).items():
            dest = output / rel
            if dest.exists():
                require(digest(dest) == sha, f'Conflicting publication object: {rel}')
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source / rel, dest)


def merge_data(sources, output):
    output.mkdir()
    index = None
    ids, routes = set(), set()
    for source_number, source in enumerate(sources):
        incoming = read(source / 'index.json')
        require(incoming.get('schema') == 'bootdisk-web-collection-1', 'Expected collection data')
        if index is None:
            index = dict(incoming);index['entries'] = [];index['media'] = []
        for medium in incoming['media']:
            require(medium['id'] not in ids, f"Medium already present: {medium['id']}")
            ids.add(medium['id']);index['media'].append(medium)
        for row in incoming['entries']:
            name = row['entry'].lower() + '.json'
            require('/' not in name and '\\' not in name and name not in routes, 'Route collision/unsafe filename')
            routes.add(name)
            # First input (the existing public collection) is copied byte-for-byte.
            if source_number == 0:
                require(len(index['entries']) == row['source_order'], 'Baseline source order is inconsistent')
                shutil.copyfile(source / name, output / name)
            else:
                row = dict(row);row['source_order'] = len(index['entries'])
                doc = read(source / name);doc['source_order'] = row['source_order'];write(output / name, doc)
            index['entries'].append(row)
    index['medium'] = f'{len(ids)} CD-er'
    write(output / 'index.json', index)


class Pipeline:
    def __init__(self, run):
        self.run = run
        self.repos = {k: Path(v) for k, v in run.plan['repositories'].items()}
        self.web = self.repos['web'] / 'scripts'
        self.env = dict(os.environ, PYTHONPATH=os.pathsep.join(str(self.repos[k]) for k in ('catalog', 'publish', 'ingest')),
                        PYTHONDONTWRITEBYTECODE='1')

    def command(self, stage, *args, output=None, executable=None):
        with (stage / 'commands.log').open('ab') as log:
            command = [str(executable or sys.executable), *map(str, args)]
            log.write((json.dumps(command) + '\n').encode());log.flush()
            if output:
                with Path(output).open('wb') as target:
                    subprocess.run(command, env=self.env, check=True, stdout=target, stderr=log)
            else:
                subprocess.run(command, env=self.env, check=True, stdout=log, stderr=log)

    def disc(self, m):
        prefix = m['id']
        def step(name, fn):
            return self.run.stage(prefix + '-' + name, fn)
        if m.get('iso'):
            source = step('source', lambda p: self.command(p, 'x', '-y', '-o' + str(p / 'files'), m['iso'],
                                                         executable=self.run.plan['seven_zip'])) / 'files'
        else:
            source = Path(m['source_root'])
        def observe(p):
            args = ['-m', 'bootdisk_ingest', source, '--output', p/'manifest.json', '--extract-to', p/'extraction']
            if m.get('iso'):
                args += ['--image', m['iso']]
            self.command(p, *args)
        obs = step('observe', observe);manifest = obs/'manifest.json';data = read(manifest)
        coverage = data.get('source', {}).get('coverage', {})
        require(not coverage.get('unprocessed_metadata') and
                not any(x.get('unprojected_sections') for x in coverage.get('metadata_files', [])),
                'Unprocessed source metadata; see observed manifest coverage')
        tools_observed = any(x.get('path', '').casefold() == 'tools.dtx' for x in coverage.get('metadata_files', []))
        require(not (m['profile'] == 'dtx-workshop' and tools_observed),
                'Root Tools.dtx already observed: workshop profile could duplicate entries')
        if m['profile'] == 'dtx':
            # Avoid accidentally treating known workshop CDs as main-menu-only.
            require(tools_observed or not any(p.name.casefold() == 'tools' for p in source.iterdir()),
                    'Tools directory without observed Tools.dtx: choose workshop profile or investigate')
        def primary(p):
            self.command(p, '-m','bootdisk_catalog.import_ingest',manifest,'--output',p/'catalog')
            self.command(p, '-m','bootdisk_publish',manifest,'--publish-images','--extraction',obs/'extraction','--output',p/'published')
            self.command(p, '-m','bootdisk_catalog.presentation',p/'catalog',manifest,output=p/'presentation.json')
            self.command(p,self.web/'build-frontend-data.py',p/'presentation.json',p/'published/publish-manifest.json','--medium',m['label'],'--output',p/'data')
        main = step('primary', primary)
        def documents(p):
            self.command(p,'-m','bootdisk_ingest.rtf_documents',manifest,source,'--output',p/'observations.json')
            self.command(p,'-m','bootdisk_catalog.source_documents',manifest,p/'observations.json',output=p/'documents.json')
            self.command(p,'-m','bootdisk_publish.documents',p/'documents.json','--output',p/'published','--manifest-output',p/'published.json')
            self.command(p,self.web/'attach-source-documents.py',main/'data',p/'published.json','--output',p/'data')
        docs = step('documents', documents)
        tools = None
        if m['profile'] == 'dtx-workshop':
            def workshop(p):
                self.command(p,'-m','bootdisk_ingest.legacy_tools',source,manifest,'--output',p/'manifest.json','--images',p/'images')
            tools = step('workshop', workshop)
            def project_tools(p):
                tm = tools/'manifest.json'
                self.command(p,'-m','bootdisk_catalog.import_ingest',tm,'--output',p/'catalog-launches')
                self.command(p,'-m','bootdisk_catalog.embedded_images',tools/'images/images.json',tm,p/'catalog-launches','--output',p/'catalog')
                self.command(p,'-m','bootdisk_publish.embedded',tools/'images/images.json',tm,'--output',p/'published')
                self.command(p,'-m','bootdisk_catalog.presentation',p/'catalog',tm,output=p/'presentation.json')
                self.command(p,self.web/'build-frontend-data.py',p/'presentation.json',p/'published/publish-manifest.json','--medium',m['label'],'--output',p/'data')
            projected = step('workshop-project', project_tools)
        def combine(p):
            screenshots = sum(bool(e.get('files',{}).get('discovered',{}).get('screenshot',{}).get('exists')) for e in data['entries'])
            write(p/'main.json',{'media':[{'id':prefix,'data':str(docs/'data'),'image_requirements':{'minimum_counts':{'screenshot':screenshots}}}]})
            self.command(p,self.web/'build-collection.py',p/'main.json','--output',p/'main')
            stores = [main/'published/store', docs/'published/store']
            if tools:
                write(p/'tools.json',{'media':[{'id':prefix,'data':str(projected/'data'),'image_requirements':{'minimum_counts':{'icon':len(read(tools/'manifest.json')['entries'])}}}]})
                self.command(p,self.web/'append-source-posts.py',p/'main',p/'tools.json','--output',p/'data')
                stores.append(projected/'published/store')
            else:
                shutil.copytree(p/'main',p/'data')
            union_store([s for s in stores if s.exists()],p/'published/store')
        combined = step('combine', combine)
        cards = [read(combined/'data'/(e['entry'].lower()+'.json')) for e in read(combined/'data/index.json')['entries']]
        require(not any(d.get('source_catalog',{}).get('machine_tasks') for d in cards), 'Source-readiness has machine tasks')
        return combined, {'id':prefix,'status':'ready_for_review','entries':len(cards),
                         'rtf_documents':sum(len(d.get('source_documents',[])) for d in cards),
                         'coverage':coverage,
                         'asset_issues':data.get('validation',{}),
                         'source_issues':[{'entry':d['entry'],'issues':d.get('source_catalog',{}).get('file_association',{})}
                                          for d in cards if d.get('source_catalog',{}).get('file_association',{}).get('issues')],
                         'unreadable_rtf':[{'entry':d['entry'],'path':r.get('path'),'warning':r.get('warning')}
                                           for d in cards for r in d.get('source_documents',[]) if not r.get('text')],
                         'scope':'Observed menus only; no complete-disc, workshop-RTF or runtime certification'}

    def aggregate(self, discs):
        def build(p):
            base = self.run.plan['baseline']
            sources = ([Path(base)/'data'] if base else []) + [d/'data' for d in discs]
            merge_data(sources,p/'data')
            stores = ([Path(base)/'store'] if base else []) + [d/'published/store' for d in discs]
            union_store(stores,p/'published/store')
            args = [self.web/'build-release.py',p/'data',p/'published','--expected-entries',len(read(p/'data/index.json')['entries']),'--output',p/'preview']
            if self.run.plan.get('collections'):
                args += ['--collections', self.run.plan['collections']]
            if base and (Path(base)/'data/public-updates.json').exists():
                # The release builder correctly rejects history for an older projection.
                # Preserve it outside the preview for the later explicit release step.
                shutil.copyfile(Path(base)/'data/public-updates.json',p/'baseline-public-updates.json')
            self.command(p,*args)
        return self.run.stage('collection',build)


def execute(config, workspace, stop_after=None):
    workspace = Path(workspace).absolute()
    require(not workspace.is_symlink(), 'Workspace cannot be a symlink')
    workspace = workspace.resolve()
    plan = load_plan(config,workspace)
    with Run(workspace,plan,stop_after) as run:
        pipeline = Pipeline(run);reports=[];discs=[]
        try:
            for m in plan['media']:
                try:
                    path, report = pipeline.disc(m);discs.append(path);reports.append(report)
                except (IntakeError, subprocess.CalledProcessError, ValueError, OSError) as exc:
                    reports.append({'id':m['id'],'status':'blocked','error':str(exc)})
            if all(r['status']=='ready_for_review' for r in reports):
                try:
                    require(load_plan(config, workspace) == plan, 'Inputs changed during processing; use a new workspace')
                    pipeline.aggregate(discs)
                except (IntakeError, subprocess.CalledProcessError, ValueError, OSError) as exc:
                    reports.append({'id':'collection','status':'blocked','error':str(exc)})
        except KeyboardInterrupt:
            reports.append({'id':'run','status':'interrupted','error':'Run the same command to resume'})
        result = {'schema':SCHEMA,'media':reports,'completed_stages':run.completed,
                  'ready_for_review':bool(reports) and all(r['status']=='ready_for_review' for r in reports),
                  'published':False,'history_pending':True}
        write(workspace/'report.json',result)
        lines=['# Innlesingsrapport','', 'Klar til gjennomgang: '+('ja' if result['ready_for_review'] else 'nei'),
               'Ingen publisering eller kurateringsbeslutninger er utført. Ny historikk opprettes først ved publisering.','']
        for r in reports:
            lines += ['## '+r['id'], '', 'Status: '+r['status'], '']
            if r.get('error'):
                lines += [r['error'], '', 'Se manifest og commands.log i CD-ens trinnmapper.', '']
            else:
                lines += [f"{r['entries']} kildeposter; {r['rtf_documents']} RTF-dokumenter.", '']
                for field, label in [('source_issues', 'Kildeavvik'), ('unreadable_rtf', 'RTF uten lesbar tekst')]:
                    lines += [f'{label}: {len(r[field])}', '']
                    lines += ['- '+json.dumps(issue, ensure_ascii=False) for issue in r[field]]
                assets = r.get('asset_issues', {})
                for field in ('missing_referenced_files', 'missing_discovered_assets', 'warnings'):
                    if assets.get(field):
                        lines += [field+': '+json.dumps(assets[field], ensure_ascii=False), '']
                lines += ['Dekning: observerte menyer. Full CD-dekning, verkstedets RTF-er og kjørbarhet er ikke sertifisert.', '']
        require(not (workspace/'report.md').is_symlink(), 'Unsafe report path')
        (workspace/'report.md').write_text('\n'.join(lines),encoding='utf-8')
        return 0 if result['ready_for_review'] else 2


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('config',type=Path);p.add_argument('--workspace',required=True,type=Path)
    p.add_argument('--stop-after',help='Controlled interruption after a named checkpoint (acceptance testing)')
    a=p.parse_args()
    try:
        return execute(a.config,a.workspace,a.stop_after)
    except (IntakeError, OSError, ValueError, KeyError) as exc:
        print(f'Innlesing stoppet: {exc}',file=sys.stderr);return 2


if __name__=='__main__':
    raise SystemExit(main())
