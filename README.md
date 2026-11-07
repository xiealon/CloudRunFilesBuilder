# CloudRunFilesBuilder · 备份分支 `25.12-honk-r2`

本分支**只存放备份**，不含任何构建代码、脚本与工作流。

## 目录

| 路径 | 内容 |
|---|---|
| `backups/immortalwrt-artifacts/` | `xiealon/immortalwrt-artifacts` 三个 r2 release 的镜像副本 |

详细校验表、恢复方式与许可说明见
[`backups/immortalwrt-artifacts/README.md`](backups/immortalwrt-artifacts/README.md)。

## 内容一览

| 子目录 | 文件 |
|---|---|
| `imagebuilder/` | ImageBuilder `tar.zst` + `sha256sums` + `SHA256SUMS` |
| `packages-x86_64/` | `packages-x86_64-25.12.2.tar.zst` 分片 `part-00 ~ part-04` + 校验文件 |
| `firmware-x86_64/` | `kernel.bin` + 3 个 `img.gz` + 校验文件 |

合计 **21 个文件 / 671.8 MB**。

## 合并分片

```sh
cd backups/immortalwrt-artifacts/packages-x86_64
cat packages-x86_64-25.12.2.tar.zst.part-0* > packages-x86_64-25.12.2.tar.zst
sha256sum -c packages-x86_64-25.12.2.tar.zst.sha256
```

合并结果 `7af7a3a914ae3876e32890150c7bf001a80d160a0ee6769796fc25669478c1a4`，
与 release 里的完整 tar 逐字节相同。

## 内核与采集时间

- 内核 **6.12.103**，hash `26ed6bc1347f7e9e86ff98fe27513539`
- 采集于 **2026-11-05**（Asia/Shanghai）

## 说明

- 本分支**不参与构建**，没有任何 workflow，也不会被定时任务触发。
- 主仓库发布被删除或资产被同名替换时，用本分支顶回去。
- 构建代码在 `master`、`extra-apk`、`extra-ipk`、`honk-apk` 等分支，与本分支无关。
