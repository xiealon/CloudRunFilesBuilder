# honk 2026.11.12-r3 · 全部产物备份

备份 **honk 2026.11.12-r3 / luci-app-honk 2026.11.12.3-r1** 的全部 **6 个** release
资产，来源为 release
[`honk-apk`](https://github.com/xiealon/CloudRunFilesBuilder/releases/tag/honk-apk)。

包由 fork [`xiealon/kenzok8-honk`](https://github.com/xiealon/kenzok8-honk) 构建
（candidate `candidate-2026.11.12.3-757e6bcd8c2a`）。

合计 **6 个文件 / 52.31 MB**。

## 文件与校验

| 文件 | 字节 | sha256 |
|---|---|---|
| `25-openwrt-honk-2026.11.12-r3-aarch64_cortex-a53.run` | 13718331 | `931d9e774216454b62d04236b3daff2f03aeba7b839fcbcdbf5d1176787efc40` |
| `25-openwrt-honk-2026.11.12-r3-aarch64_generic.run` | 13718363 | `c436d90f434b7e3733946a2b4b05f2d497f4a2a835e3b106cca773cead282ea2` |
| `25-openwrt-honk-2026.11.12-r3-x86_64.run` | 14416970 | `326dad7ba1e205eb58e3f6aba13567a6b6ff353f2c1071d2054efcdfec9ac9f3` |
| `README.md` | 1528 | `2d1d6b6151bd7cf00af693771d5647e96402ee37a61105e93af7e548267838bb` |
| `SHA256SUMS` | 107 | `38b4b4d8e7b175e17983eff3abc17933b77ec5229d2ba74465fc2c9d345afe19` |
| `honk-2026.11.12-r3-x86_64.apk` | 12991132 | `6d82a0e3e7905dc1b6053730295a874879f25c805b8acaa7dc696f4e3e75ac25` |

## r3 改了什么

`config.dae` 自带 `global` 段，honk 因此判定「设置由文件托管」
（`config_settings_owned_by_file`），从此不再按 uci 生成 `system.dae`。
后果：只打开 `clash_api_enabled` 也永远不会出现 `clash_api` 块，9090 不监听。

r3 把块直接预置进包内 `system.dae`：

```
    clash_api {
        external_controller: '0.0.0.0:9090'
        external_ui: '/usr/share/honk/zashboard'
        secret: 'honk-9090-placeholder'
        default_mode: Rule
    }
```

`/etc/uci-defaults/90-honk` 首次开机把占位 secret 换成 16 位随机值，
因此每台机器密码不同，**无需进 LuCI 保存应用**即可用 9090。

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
