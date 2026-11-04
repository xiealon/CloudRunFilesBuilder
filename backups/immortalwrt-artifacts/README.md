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

## 不用合并的地方

Release `backup-immortalwrt-artifacts-20261104` 里是完整文件，下载即用。

## 内核

kernel 6.12.103，hash `26ed6bc1347f7e9e86ff98fe27513539`。

## 采集时间

2026-11-05（Asia/Shanghai）

## 主仓库失效时怎么顶替

`xiealon/immortalwrt-artifacts` 被删、或资产被同名静默替换时，用本备份顶回去。三种方式任选。

### 方式一：重建主仓库 release（推荐）

文件名与本备份完全一致，不用改名、不用合并。

1. 在主仓库按同名 tag 建三个 release：
   - `v25.12.2-ib-x86-64-r2`
   - `v25.12.2-pkg-x86-64-r2`
   - `v25.12.2-fw-x86-64-r2`
2. 从本备份下载对应文件，原样上传
3. 核对：

```sh
sha256sum -c sha256sums --ignore-missing
```

workflow 里的 `IB_SHA` / `PKG_SHA` 不用动 —— 那两个值钉的是内容，内容没变。

### 方式二：不改主仓库，让 workflow 直接指过来

改 `ImmortalWrt-ImageBuilder-25.12-honk` 的 `.github/workflows/build-x86-64-25.12.x.yml` 第 377、411 行：

```yaml
IB_URL="https://github.com/xiealon/CloudRunFilesBuilder/releases/download/backup-immortalwrt-artifacts-20261104/immortalwrt-imagebuilder-25.12.2-x86-64.Linux-x86_64.tar.zst"
PKG_URL="https://github.com/xiealon/CloudRunFilesBuilder/releases/download/backup-immortalwrt-artifacts-20261104/packages-x86_64-25.12.2.tar.zst"
```

378、412 两行 SHA 保持原值不变。

### 方式三：用分支副本顶替

分支 `25.12-honk-r2` 的 `backups/immortalwrt-artifacts/` 里是拆片，先合并：

```sh
cat packages-x86_64/packages-x86_64-25.12.2.tar.zst.part-0* > packages-x86_64-25.12.2.tar.zst
sha256sum -c packages-x86_64/packages-x86_64-25.12.2.tar.zst.sha256
```

合并结果与 release 里的 tar 逐字节相同（`7af7a3a9…78c1a4`）。

### 校验基准

任一文件的 sha 与本表不符，就是被换过。

| 文件 | 字节 | sha256 |
|---|---|---|
| immortalwrt-imagebuilder-25.12.2-x86-64.Linux-x86_64.tar.zst | 63,177,329 | `73abe42d053fbc5a261235c08142704cdc253ff9e05ea7b9e0e2cb5e75b312e8` |
| packages-x86_64-25.12.2.tar.zst | 331,366,482 | `7af7a3a914ae3876e32890150c7bf001a80d160a0ee6769796fc25669478c1a4` |
| immortalwrt-25.12.2-x86-64-generic-kernel.bin | 7,910,400 | `52adb2487f8004a07cf806d446499393650733f8d02149f2340fe26d074a36de` |
| immortalwrt-25.12.2-x86-64-generic-squashfs-combined-efi.img.gz | 103,431,643 | `134a7c9ed77b6f43e877a1266e07874d2d47873e42b97d65ce1737e7fc4ccdaf` |
| immortalwrt-25.12.2-x86-64-generic-squashfs-combined.img.gz | 103,228,039 | `3f09cec88785d39ca27a9bd1d6db276ed4e6d7a73b7ba6dd1dd9871a72980152` |
| immortalwrt-25.12.2-x86-64-generic-squashfs-rootfs.img.gz | 94,905,090 | `348623827be3a1ebead47a66e9401dd86eb5c881fd31935d00be1c851d6b71e5` |
| sha256sums | 146,295 | `92c33f548bb947ca1d5c65855f6a251f8fd90f0b7ec5d4cb4bc6ebf86f0fc374` |

## 许可

MIT，见本目录的 `LICENSE` 与 `LICENSE.md`。
