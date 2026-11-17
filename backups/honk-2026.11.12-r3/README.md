# honk 2026.11.12-r3 · 全部产物备份

备份 **honk 2026.11.12-r3 / luci-app-honk 2026.11.12.3-r1** 的全部 **1 个** release
资产，来源为 release
[`honk-apk`](https://github.com/xiealon/CloudRunFilesBuilder/releases/tag/honk-apk)。

合计 **1 个文件 / 1.40 MB**。

## 文件与校验

| 文件 | 字节 | sha256 |
|---|---|---|
| `luci-app-honk-2026.11.12.3-r1-x86_64.apk` | 1465972 | `a71ee71dd0a25fcad6bcd0d219e3178357cd42ea3977bb88fa6ae6487df12a74` |

## r3 相对 r2 的改动

`config.dae` 自带 `global` 段，honk 因此判定「设置由文件托管」
（`config_settings_owned_by_file`），从此不再按 uci 生成 `system.dae` —— 只开
`clash_api_enabled` 也永远不会出现 `clash_api` 块，9090 不监听。

r3 把 `clash_api` 块直接预置进包内 `system.dae`：

```
    clash_api {
        external_controller: '0.0.0.0:9090'
        external_ui: '/usr/share/honk/zashboard'
        secret: 'honk-9090-placeholder'
        default_mode: Rule
    }
```

`/etc/uci-defaults/90-honk` 首次开机把占位 secret 换成 16 位随机值，
因此每台机器密码不同，且**无需进 LuCI 保存应用**即可用 9090。

## 用法

```sh
chmod +x 25-openwrt-honk-2026.11.12-r3-x86_64.run
./25-openwrt-honk-2026.11.12-r3-x86_64.run
```

```sh
apk add --allow-untrusted honk-2026.11.12-r3-x86_64.apk \
                        luci-app-honk-2026.11.12.3-r1-x86_64.apk
```

要求：Linux >= 6.12 且 `CONFIG_DEBUG_INFO_BTF=y`。

## 校验

```sh
sha256sum -c SHA256SUMS
```
