# honk 2026.11.12-r2 · 全部产物备份

本目录备份 **honk 2026.11.12-r2 / luci-app-honk 2026.11.12.3-r1** 的全部 **5 个**
release 资产，来源为本仓库 release
[`honk-apk`](https://github.com/xiealon/CloudRunFilesBuilder/releases/tag/honk-apk)。

包由 fork [`xiealon/kenzok8-honk`](https://github.com/xiealon/kenzok8-honk) 构建
（candidate `candidate-2026.11.12.3-e79fc1c5e7ce`）。

合计 **5 个文件 / 53.70 MB**。

## 文件与校验

| 文件 | 字节 | sha256 |
|---|---|---|
| `25-openwrt-honk-2026.11.12-r2-aarch64_cortex-a53.run` | 13718703 | `eb702068cab7962540ac54e635ba5a91949888db95cfa923852b8ab7e97ccb13` |
| `25-openwrt-honk-2026.11.12-r2-aarch64_generic.run` | 13718233 | `820b3e639b11bfcfae9bf1c177d4ea8dbf36f1cebdd7edc54671548af2db530f` |
| `25-openwrt-honk-2026.11.12-r2-x86_64.run` | 14416720 | `5803eda1c3247a6ded9f3ee7c47c8b2b8dbf4a546e3ff237c1f9b088235bd79a` |
| `honk-2026.11.12-r2-x86_64.apk` | 12991103 | `760c016d7d31cb6ceb4c54a5030ad9456eb39e932a7d55691327828b3c43bab4` |
| `luci-app-honk-2026.11.12.3-r1-x86_64.apk` | 1465972 | `a71ee71dd0a25fcad6bcd0d219e3178357cd42ea3977bb88fa6ae6487df12a74` |

## 这一版相对 r1 的改动

1. `honk/files/90-honk-boot`（uci-defaults）：首次安装时把 `clash_api_enabled` 置 1、
   生成 16 位随机 `clash_api_secret`，于是 `control.sh` 会往 `/etc/honk/system.dae`
   写 `clash_api {}` 块，**9090 开箱可用**。代理本体仍需用户显式启用
   （`honk.main.enabled`），安全默认不变。
2. `luci-app-honk` 升到 `2026.11.12.3`（移除 Package updates 卡片）。

## 用法

自解压包（3 个，三架构）：

```sh
chmod +x 25-openwrt-honk-2026.11.12-r2-x86_64.run
./25-openwrt-honk-2026.11.12-r2-x86_64.run
```

散装 apk（2 个，给 ImageBuilder 装进固件）：

```sh
apk add --allow-untrusted honk-2026.11.12-r2-x86_64.apk \
                        luci-app-honk-2026.11.12.3-r1-x86_64.apk
```

要求：Linux >= 6.12 且 `CONFIG_DEBUG_INFO_BTF=y`。

## 校验

```sh
sha256sum -c SHA256SUMS
```
