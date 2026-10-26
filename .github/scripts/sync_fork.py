# -*- coding: utf-8 -*-
"""把 fork 仓库(xiealon/store, xiealon/apk)里的包同步成固定文件名的 .run。

用法:
  python sync_fork.py --dry-run                       # 只打印映射
  python sync_fork.py --repo store --outdir out/ipk   # 下载 + 打包（需 makeself）
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request as U

HERE = os.path.dirname(os.path.abspath(__file__))
PROXY = os.environ.get('SYNC_PROXY', '')
if PROXY:
    U.install_opener(U.build_opener(U.ProxyHandler({'http': PROXY, 'https': PROXY})))

ARCH_SEG = re.compile(r'^(x86[-_]?64|x86|all|aarch64|arm64|a53|generic|cortex)$', re.I)
ARCH_SUFFIX = re.compile(r'[-_](x86[-_]64|aarch64_[a-z0-9_\-]+|arm64|all)$', re.I)
DIGIT_SEG = re.compile(r'^v?\d')

# 少数命名不规整的，直接钉死
OVERRIDE = {
    'ssrp_mihomo_x86_64-196_r2.run': 'ssrp',
    '24-luci-app-dead_1.28-x86-64.run': 'luci-app-dead',
    'AdGuardHome_v0.107.72_x86_64.run': 'adguardhome',
    'homeproxy-x86_64-26.126.28706-6ac4a03.run': 'homeproxy',
    '24_quickfile_1.0.16_x86_64.run': 'quickfile',
    '25_PassWall_26.6.2_x86_64.run': 'passwall',
    'libs': 'libs',
}


def token():
    for key in ('GH_TOKEN', 'GITHUB_TOKEN', 'SYNC_TOKEN'):
        v = os.environ.get(key)
        if v:
            return v
    for f in glob.glob(os.path.join(HERE, '*.py')):
        s = open(f, encoding='utf-8', errors='ignore').read()
        for m in re.finditer(r'gh[pousr]_[A-Za-z0-9_]{30,}', s):
            t = m.group(0)
            try:
                U.urlopen(U.Request('https://api.github.com/user', headers={'Authorization': 'Bearer ' + t, 'User-Agent': 'w'}), timeout=20).read()
                return t
            except Exception:
                continue
    return None


def get(url, tok):
    return json.load(U.urlopen(U.Request(url, headers={'User-Agent': 'w', 'Authorization': 'Bearer ' + tok}), timeout=60))


def canon(name, arch):
    """<app>[_<ver>][_<arch>].run -> <app>_<arch>.run"""
    if name in OVERRIDE:
        return '%s_%s.run' % (OVERRIDE[name], arch)
    base = re.sub(r'\.run$', '', name)
    base = re.sub(r'^2[45][-_]', '', base)          # 24_ / 25- 前缀
    base = ARCH_SUFFIX.sub('', base)
    segs = [s for s in re.split(r'[-_]', base) if s]
    app = []
    for s in segs:
        if ARCH_SEG.match(s) or DIGIT_SEG.match(s):
            break
        app.append(s)
    if not app:
        app = segs[:1] or [base]
    return '%s_%s.run' % ('-'.join(app), arch)


def build_plan(repo, arch, tok, suffix=None):
    suffix = suffix or arch
    items = get('https://api.github.com/repos/%s/contents/run/%s' % (repo, arch), tok)
    plan = []
    for x in items:
        if x['type'] == 'file' and x['name'].endswith('.run'):
            plan.append({'kind': 'run', 'src_name': x['name'], 'url': x['download_url'],
                         'size': x['size'], 'out': canon(x['name'], suffix)})
        elif x['type'] == 'dir':
            sub = get('https://api.github.com/repos/%s/contents/run/%s/%s' % (repo, arch, x['name']), tok)
            files = [s for s in sub if s['type'] == 'file']
            if not files:
                continue
            plan.append({'kind': 'dir', 'src_name': x['name'], 'files': files,
                         'size': sum(f.get('size', 0) for f in files),
                         'out': '%s_%s.run' % (OVERRIDE.get(x['name'], x['name']), suffix)})
    return plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--repo', default='')
    ap.add_argument('--arch', default='x86')
    ap.add_argument('--suffix', default='x86_64')
    ap.add_argument('--outdir', default='out')
    a = ap.parse_args()
    tok = token()

    targets = []
    if a.repo:
        targets = [(a.repo, a.outdir)]
    else:
        targets = [('xiealon/store', 'out/ipk'), ('xiealon/apk', 'out/apk')]

    for repo, outdir in targets:
        try:
            plan = build_plan(repo, a.arch, tok, a.suffix)
        except Exception as e:
            print('%s 读取失败: %s' % (repo, e))
            continue
        print('=' * 72)
        print('%s/run/%s  ->  %s   共 %d 项，%.2f MB' % (
            repo, a.arch, outdir, len(plan), sum(p['size'] for p in plan) / 1048576.0))
        print('=' * 72)
        for p in sorted(plan, key=lambda y: y['out']):
            print('  %-46s %8.2f MB  ->  %-28s [%s]' % (
                p['src_name'], p['size'] / 1048576.0, p['out'], p['kind']))
        if a.dry_run:
            continue

        os.makedirs(outdir, exist_ok=True)
        stage = os.path.join(outdir, '_stage')
        shutil.rmtree(stage, ignore_errors=True)
        os.makedirs(stage, exist_ok=True)
        for p in plan:
            d = os.path.join(stage, p['out'][:-4])
            shutil.rmtree(d, ignore_errors=True)
            os.makedirs(d, exist_ok=True)
            if p['kind'] == 'run':
                dst = os.path.join(d, os.path.basename(p['url']))
                urllib_dl(p['url'], dst)
                # 源本身就是打好包的 .run，直接改名，不再二次打包
                shutil.move(dst, os.path.join(outdir, p['out']))
                continue
            else:
                for f in p['files']:
                    urllib_dl(f['download_url'], os.path.join(d, f['name']))
                ext = '.apk' if any(f['name'].endswith('.apk') for f in p['files']) else '.ipk'
                ins = os.path.join(d, 'install.sh')
                if ext == '.ipk':
                    open(ins, 'w', newline='\n').write(
                        '#!/bin/sh\nopkg update || exit 1\nopkg install ./*.ipk\n')
                else:
                    open(ins, 'w', newline='\n').write(
                        '#!/bin/sh\napk update || exit 1\napk add --allow-untrusted ./*.apk\n')
                os.chmod(ins, 0o755)
            subprocess.check_call([os.environ.get('MAKESELF', 'makeself'), d, os.path.join(outdir, p['out']),
                                   p['out'][:-4], './install.sh'])
        shutil.rmtree(stage, ignore_errors=True)
        print('产出目录 %s:' % outdir)
        for f in sorted(glob.glob(os.path.join(outdir, '*.run'))):
            print('  %-42s %.2f MB' % (os.path.basename(f), os.path.getsize(f) / 1048576.0))


def urllib_dl(url, dst):
    data = U.urlopen(U.Request(url, headers={'User-Agent': 'w'}), timeout=900).read()
    open(dst, 'wb').write(data)


if __name__ == '__main__':
    main()
