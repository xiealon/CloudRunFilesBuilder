# 四仓库源码备份 · 2026-11-18

按仓库分四个子目录，逐文件保存 `master` 当时内容（不含 `.git`）：

| 目录 | 说明 |
|---|---|
| `ImmortalWrt-ImageBuilder-25.12-honk/` | honk 线 |
| `ImmortalWrt-ImageBuilder-25.12-daed/` | daed 线（本次定版所用） |
| `ImmortalWrt-ImageBuilder-25.12/` | 官方 25.12 线 |
| `ImmortalWrt-ImageBuilder-24.10/` | 官方 24.10 线（opkg 体系） |

含本轮全部修复：manifest 反查、去重跳过 kmod、C3 全量 kmod、honk/daed 清单 token 鉴权、
`_PA_DAED` 正名 + geo、LuCI 缓存清理、单包重试、95-luci 进主流程、apk 非 0 判成功、
rc.local 清单兜底 `--all`、SCRIPT_VER `2026-11-18.1245`。

固件产物在各自仓库 release；honk 包在 `backups/honk-2026.11.12-r3/`。
