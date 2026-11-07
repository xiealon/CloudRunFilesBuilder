# honk 0.1.0_beta5-r1 · 全部产物备份

本目录备份 **honk 0.1.0_beta5-r1** 的全部 **8 个** release 资产，来源为本仓库
release [`honk-apk`](https://github.com/xiealon/CloudRunFilesBuilder/releases/tag/honk-apk)，
对应上游 [`daeuniverse/honk` v0.1.0-beta.5](https://github.com/daeuniverse/honk/releases/tag/v0.1.0-beta.5)。

合计 **8 个文件 / 60.67 MB**。

> 上一代 `0.1.0_beta4-r3` 仍在同级目录 `backups/honk-0.1.0_beta4-r3/`。

## 文件与校验

| 文件 | 字节 | sha256 |
|---|---|---|
| `25-openwrt-honk-0.1.0_beta5-r1-aarch64_cortex-a53.run` | 15551407 | `92c878e10c7dbfa691918d106e7418a9c5da7edde43d3199becdaef028a213de` |
| `25-openwrt-honk-0.1.0_beta5-r1-aarch64_generic.run` | 15551495 | `7c4217f56bf30db975a85ed76da6ed4c49297d4af80a648add22c2c805637653` |
| `25-openwrt-honk-0.1.0_beta5-r1-x86_64.run` | 16224658 | `df984d4e5cf149e84456ccd1715501899b6236331547abf2b084ccfd71bba016` |
| `honk-0.1.0_beta5-r1.apk` | 16271128 | `3e87802f7d6ba63e4ebb6114a9ef92167b6b304d7eb163a85879818dd93a0781` |
| `luci-app-honk-26.307.37363.6742962.apk` | 4950 | `b80020fd11f7a61e9733a6efebd4b0736516d40f035aa0d4d720726cd57a692c` |
| `luci-i18n-daeuniverse-zh-cn-26.307.37363.6742962.apk` | 2810 | `5ba0e22bdc4db29890e706ea730a049dd15deec414bf923318f145f902ce3ed6` |
| `luci-lib-daeuniverse-26.307.37363.6742962.apk` | 11928 | `56e0ce6ea195e6b90b39888b755f0e6ae2a4add200c500540d68ef2e992d92ed` |
| `vmlinux-btf-builtin-1-r1.apk` | 970 | `399da2d5d7fbf26154dc21fa4a288a420554c73dcbd1b3fd94df1628455a9df2` |

## 两类产物

**一、自解压包（3 个 `.run`，三架构）**：路由器上直接跑

```sh
chmod +x 25-openwrt-honk-0.1.0_beta5-r1-x86_64.run
./25-openwrt-honk-0.1.0_beta5-r1-x86_64.run
```

**二、散装 apk（5 个，x86_64）**：给 ImageBuilder 装进固件，即 `_PA_HONK` 保护组五件套

| 包 | 说明 |
|---|---|
| `honk` | eBPF 透明代理引擎（dae 的独立实现） |
| `luci-app-honk` | LuCI 界面（服务 → Honk） |
| `luci-lib-daeuniverse` | LuCI 依赖库 |
| `luci-i18n-daeuniverse-zh-cn` | 中文翻译 |
| `vmlinux-btf-builtin` | BTF 哨兵（1 B，装前检查 `/sys/kernel/btf/vmlinux`） |

## 启用

```sh
uci set honk.config.enabled=1 && uci commit honk
/etc/init.d/honk enable && /etc/init.d/honk start
```

## 要求与冲突

- 内核 **>= 6.12** 且 `CONFIG_DEBUG_INFO_BTF=y`
- **honk 与 dae / daed 互斥**：都占用 `dae0` 设备与 `daens` 命名空间

## 校验

```sh
sha256sum -c SHA256SUMS
```

## 关于 Source code

release 页面上的 `Source code (zip/tar.gz)` 是 GitHub 按 tag 自动打包的仓库源码快照，
不是 honk 产物，因此不在本目录备份。

## 归档说明

- 本目录只存产物，不含源码
- release 若被删除或资产被同名替换，用本目录顶回去
- 采集于 **2026-11-08**（Asia/Shanghai）
