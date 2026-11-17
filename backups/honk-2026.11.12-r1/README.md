# honk 2026.11.12-r1 · 全部产物备份

本目录备份 **honk 2026.11.12-r1** 的全部 **5 个** release 资产，来源为本仓库
release [`honk-apk`](https://github.com/xiealon/CloudRunFilesBuilder/releases/tag/honk-apk)。

与历史上游备份不同，这一版**并非上游原样**：包由 fork
[`xiealon/kenzok8-honk`](https://github.com/xiealon/kenzok8-honk) 构建，
`/etc/honk/config.dae` 已按使用者自己的分组策略定制（见下）。

合计 **5 个文件 / 53.70 MB**。

## 文件与校验

| 文件 | 字节 | sha256 |
|---|---|---|
| `25-openwrt-honk-2026.11.12-r1-aarch64_cortex-a53.run` | 13718475 | `0d17e9e5b87076368bb6b1dd3a195d095f59eff6ade91d006b638317d2f6034a` |
| `25-openwrt-honk-2026.11.12-r1-aarch64_generic.run` | 13717914 | `573cf91e60c8e3d41e5fd4230b4b1927535bf69e3c6463c9eac26f3f8dda7fb4` |
| `25-openwrt-honk-2026.11.12-r1-x86_64.run` | 14416455 | `5f4c686fa33a126b05eb0b1293f9c046e301de742ad4c013fdab9594c0580c0c` |
| `honk-2026.11.12-r1-x86_64.apk` | 12991011 | `c345eaf4863b6979b67d0ddc12981be19b6df559e127f0da0e95fe38d7ffd3e0` |
| `luci-app-honk-2026.11.12.2-r1-x86_64.apk` | 1466054 | `2185ba6ac2639566b0219fe3aac65864e14dffec5eac3bab1002cd959f086b3f` |

## 与上游默认配置的差异

`honk/files/config.dae`（打包进 `etc/honk/config.dae`，sha256 `b0125527…4b0`）：

- 分组：`proxy` / `auto` / `youtube` / `google` / `github` / `media` / `telegram` /
  `game` / `ai` / `netflix` / `bahamut`，以及国家子组 `hk` / `ao` / `tw` / `us` /
  `sg` / `jp` / `kr` / `vn`
- 聚合组用 `filter: group(<子组>)` 引用子组；`policy` 用 `score`（honk 内置评分策略，
  不是 clash 的 select）与 `select`
- 补回了 `# honk:local-direct-begin` / `# honk:local-direct-end` 标记块
  （`scripts/check.sh:228` 要求整行精确匹配；honk 启动时靠它注入本机管理地址直连规则）
- 全文缩进统一 4 空格/层

## 用法

自解压包（3 个，三架构）：

```sh
chmod +x 25-openwrt-honk-2026.11.12-r1-x86_64.run
./25-openwrt-honk-2026.11.12-r1-x86_64.run
```

散装 apk（2 个，给 ImageBuilder 装进固件）：

```sh
apk add --allow-untrusted honk-2026.11.12-r1-x86_64.apk \
                        luci-app-honk-2026.11.12.2-r1-x86_64.apk
```

要求：Linux >= 6.12 且 `CONFIG_DEBUG_INFO_BTF=y`。

## 校验

```sh
sha256sum -c SHA256SUMS
```
