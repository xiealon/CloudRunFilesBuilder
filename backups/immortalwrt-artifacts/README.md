# immortalwrt-artifacts 备份（r2，内核 26ed6bc1）

本目录是 `xiealon/immortalwrt-artifacts` 三个 r2 release 的镜像副本。

| 目录 | 内容 |
|---|---|
| `imagebuilder/` | ImageBuilder tar.zst + sha256sums + SHA256SUMS |
| `packages-x86_64/` | pkg 拆片 part-00 ~ part-04 + sha256sums + SHA256SUMS |
| `firmware-x86_64/` | kernel.bin + 3 个 img.gz + sha256sums + SHA256SUMS |

## 合并拆片

```sh
cat packages-x86_64-25.12.2.tar.zst.part-0* > packages-x86_64-25.12.2.tar.zst
sha256sum -c packages-x86_64-25.12.2.tar.zst.sha256
```

## 完整文件

不想合并的，直接去 Release `backup-immortalwrt-artifacts-20261104`，那里是完整文件。

## 内核

kernel 6.12.103，hash `26ed6bc1347f7e9e86ff98fe27513539`。

## 采集时间

2026-11-05（Asia/Shanghai）
