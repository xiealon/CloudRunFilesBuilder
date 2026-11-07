# honk 0.1.0_beta4-r3 · 全部产物备份

本目录备份 **honk 0.1.0_beta4-r3** 的全部 **8 个** release 资产，来源为本仓库
release [`honk-apk`](https://github.com/xiealon/CloudRunFilesBuilder/releases/tag/honk-apk)
（2026-11-02 06:21 UTC 发布，由 `github-actions` 自动构建）。

合计 **8 个文件 / 60.36 MB**。

## 文件与校验

| 文件 | 字节 | sha256 | 说明 |
|---|---|---|---|
| `25-openwrt-honk-0.1.0_beta4-r3-aarch64_cortex-a53.run` | 15475529 | `22c59ef3f66241d0ce2eb82e6b0dd030d61da4c98d0cc2547138fd46620409d4` | 自解压包 · aarch64 cortex-a53（路由器直接跑） |
| `25-openwrt-honk-0.1.0_beta4-r3-aarch64_generic.run` | 15475763 | `739fe5f435b67e2c119b736cb608e6eb2575b9fc0bb031051210b36c490eb968` | 自解压包 · aarch64 generic（路由器直接跑） |
| `25-openwrt-honk-0.1.0_beta4-r3-x86_64.run` | 16136681 | `e17142e44a139853e0f3cc4a0c75646946a8e71923f94914d371a2c1ed11075b` | 自解压包 · x86_64（路由器直接跑） |
| `honk-0.1.0_beta4-r3.apk` | 16186820 | `ce57c83dd30b8f56b5f269f12bedb8e38c661957c934353c59f7b118e6f738e5` | eBPF 透明代理引擎（dae 的独立实现） |
| `luci-app-honk-26.303.60580.1046d3c.apk` | 2734 | `99bb8d4e7a300578665416f373971004e98c00ce16dd51a03854841780c9736e` | LuCI 界面（服务 → Honk） |
| `luci-i18n-daeuniverse-zh-cn-26.303.60580.1046d3c.apk` | 2319 | `6ec3833b8a0651e4f0a6d9645bfe5a5afe4ecc992b4fdb4e7ea2ce966a69d9cd` | 中文翻译 |
| `luci-lib-daeuniverse-26.303.64947.503cdb1.apk` | 10646 | `120881d8207c66176f92b491abaf00658189545fa1bf063e922b09a60763c009` | LuCI 依赖库 |
| `vmlinux-btf-builtin-1-r1.apk` | 972 | `568e61ed1e19c2b290fbc8d80809ce86a160bac1f703907c9443283f332376dc` | BTF 哨兵（装前检查 /sys/kernel/btf/vmlinux） |

## 两类产物

**一、自解压包（3 个 `.run`，三架构）**

路由器上直接跑：

| 架构 | 文件 |
|---|---|
| x86_64 | `25-openwrt-honk-0.1.0_beta4-r3-x86_64.run` |
| aarch64 cortex-a53 | `25-openwrt-honk-0.1.0_beta4-r3-aarch64_cortex-a53.run` |
| aarch64 generic | `25-openwrt-honk-0.1.0_beta4-r3-aarch64_generic.run` |

```sh
chmod +x 25-openwrt-honk-0.1.0_beta4-r3-x86_64.run
./25-openwrt-honk-0.1.0_beta4-r3-x86_64.run
```

**二、散装 apk（5 个，x86_64）**

给 ImageBuilder 构建时装进固件，就是 `_PA_HONK` 保护组的五件套：

| 包 | 说明 |
|---|---|
| `honk` | eBPF 透明代理引擎（dae 的独立实现） |
| `luci-app-honk` | LuCI 界面（服务 → Honk） |
| `luci-lib-daeuniverse` | LuCI 依赖库 |
| `luci-i18n-daeuniverse-zh-cn` | 中文翻译 |
| `vmlinux-btf-builtin` | BTF 哨兵（1 B，装前检查 `/sys/kernel/btf/vmlinux`） |

## 启动

装完**默认不启动**，到 LuCI「服务 → Honk」开关，或：

```sh
uci set honk.config.enabled=1 && uci commit honk
/etc/init.d/honk enable && /etc/init.d/honk start
```

## 要求与冲突

- 内核 **>= 6.12** 且 `CONFIG_DEBUG_INFO_BTF=y`
- **honk 与 dae / daed 互斥**：都占用 `dae0` 设备与 `daens` 命名空间，
  同机只能留一个

## 校验

```sh
sha256sum -c SHA256SUMS
```

## 关于 Source code

release 页面上另有 `Source code (zip)` 与 `Source code (tar.gz)`，
那是 GitHub 按 tag 自动打包的**本仓库源码快照**，不是 honk 产物，
因此不在本目录备份。

## 归档说明

- 本目录只存产物，不含源码
- release 若被删除或资产被同名替换，用本目录顶回去
- 采集于 **2026-11-08**（Asia/Shanghai）
