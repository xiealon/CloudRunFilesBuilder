#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SDK 产物收集 + 运行时依赖闭包。

用法:
    depclose.py <sdk_dir> <app> <pat_regex> <out_dir>

做法:
  1. 用 PAT 从 bin/packages 里挑出本应用的"种子"包（与旧规则一致）；
  2. 读 SDK 自己生成的 bin/packages/<arch>/<feed>/Packages 索引，
     按 Depends 递归展开运行时依赖；
  3. 设备出厂就有的基础包（libc / luci-base / kmod-* / dnsmasq …）命中白名单，
     不打进 run，避免每个 run 从 20MB 涨到 200MB；
  4. 索引里查不到的依赖（本轮没编译出来）打印 MISSING，人工判断要不要补编；
  5. 只复制最终集合。

这样 run 里就自带 geo2txt / v2ray-geoip 这类"别人没想到"的依赖，
用户 opkg install 时不会卡在 cannot find dependency。
"""
import fnmatch
import glob
import os
import re
import shutil
import sys

# 设备上一定已有、或绝对不能跟着 run 走的包。
# kmod-* 必须排除：SDK 内核版本和用户设备未必一致，强装 kmod 会砖。
WHITE = [
    'libc', 'libgcc*', 'libstdcpp*', 'libpthread', 'librt', 'libm', 'libdl',
    'ld-musl*', 'libssp*', 'ca-bundle', 'ca-certificates*',
    'ucode', 'ucode-mod-*', 'uclient-fetch', 'libustream-*',
    'libubox*', 'libubus*', 'libuci*', 'libblobmsg*', 'libnl-*',
    'zlib*', 'libopenssl*', 'libmbedtls*', 'libcurl*', 'libjson-c*',
    'libcap*', 'libpcre*', 'terminfo*', 'zoneinfo-*',
    'luci-base', 'luci-compat', 'luci-lib-*', 'luci-mod-*',
    'rpcd*', 'opkg', 'busybox*',
    'kmod-*', 'kernel*',
    'firewall4', 'nftables*', 'libnftnl*', 'libmnl*',
    'iptables*', 'ip6tables*', 'ip-full', 'ip-tiny',
    'dnsmasq*', 'odhcpd*', 'dropbear*', 'openssh-*',
    'logd', 'ubox*', 'ubus', 'netifd', 'procd*', 'jsonfilter', 'jshn',
    'libiwinfo*', 'resolveip', 'libstdcpp*',
]


def dep_groups(val):
    """Depends 字符串 -> 若干"任选其一"的组。'a (>=1), b | c' -> [['a'], ['b','c']]"""
    groups = []
    for part in (val or '').split(','):
        part = part.split('(')[0].strip()
        alts = [a.strip() for a in part.split('|') if a.strip()]
        if alts:
            groups.append(alts)
    return groups


def is_white(name):
    return any(fnmatch.fnmatch(name, w) for w in WHITE)


def load_index(sdk):
    """解析 bin/packages/*/*/Packages -> {包名: {'deps': [[别名组]...], 'file': ipk路径}}"""
    idx = {}
    for pf in sorted(glob.glob(os.path.join(sdk, 'bin', 'packages', '*', '*', 'Packages'))):
        base = os.path.dirname(pf)
        cur = None
        try:
            fh = open(pf, encoding='utf-8', errors='ignore')
        except OSError:
            continue
        with fh:
            for raw in fh:
                line = raw.rstrip('\r\n')
                if not line.strip():
                    cur = None
                    continue
                if line[0] in ' \t':
                    continue          # Description 续行
                key, sep, val = line.partition(':')
                if not sep:
                    continue
                key, val = key.strip(), val.strip()
                if key == 'Package':
                    cur = {'deps': [], 'file': None}
                    idx.setdefault(val, cur)
                elif cur is None:
                    continue
                elif key == 'Depends':
                    cur['deps'] = dep_groups(val)
                elif key == 'Filename':
                    p = val[2:] if val.startswith('./') else val
                    cur['file'] = os.path.normpath(os.path.join(base, p))
    return idx


def main():
    if len(sys.argv) < 5:
        print(__doc__)
        return 2
    sdk, app, pat, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    rx = re.compile(pat)
    ipk_seeds, apk_seeds = {}, []
    for f in glob.glob(os.path.join(sdk, 'bin', 'packages', '*', '*', '*')):
        bn = os.path.basename(f)
        if not os.path.isfile(f):
            continue
        if not rx.search(bn):
            continue
        if bn.endswith('.ipk'):
            ipk_seeds[bn.split('_')[0]] = f
        elif bn.endswith('.apk'):
            apk_seeds.append(f)

    idx = load_index(sdk)
    keep, missing, seen = {}, set(), set()
    queue = list(ipk_seeds)
    while queue:
        name = queue.pop()
        if name in seen:
            continue
        seen.add(name)
        node = idx.get(name)
        if node is None:
            if name in ipk_seeds:
                keep[name] = ipk_seeds[name]
            continue
        path = node['file']
        if path and os.path.exists(path):
            keep[name] = path
        elif name in ipk_seeds:
            keep[name] = ipk_seeds[name]
        else:
            missing.add('%s (索引有、本轮没生成 ipk)' % name)
        for alts in node['deps']:
            if any(is_white(a) for a in alts):
                continue
            hit = next((a for a in alts if a in idx or a in ipk_seeds), None)
            if hit:
                if hit not in seen:
                    queue.append(hit)
            else:
                missing.add(' | '.join(alts))

    files = sorted(set(list(keep.values()) + apk_seeds))
    os.makedirs(out, exist_ok=True)
    total = 0
    for f in files:
        if not os.path.exists(f):
            print('!! 文件不存在: %s' % f)
            continue
        shutil.copy2(f, out)
        total += os.path.getsize(f)

    print('== %s: 收集 %d 个包，共 %.2f MB ==' % (app, len(files), total / 1048576.0))
    for f in sorted(files, key=lambda x: -os.path.getsize(x)):
        print('   %8.2f KB  %s' % (os.path.getsize(f) / 1024.0, os.path.basename(f)))
    if missing:
        print('== %s: 没在 run 内解决的依赖（设备需自带，或需要补编）==' % app)
        for m in sorted(missing):
            print('   MISSING  %s' % m)
    return 0 if files else 3


if __name__ == '__main__':
    sys.exit(main())
