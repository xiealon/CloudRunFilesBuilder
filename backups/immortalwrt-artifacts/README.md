# immortalwrt-artifacts 离线备份

**来源**：https://github.com/xiealon/immortalwrt-artifacts
**备份时间**：2026-11-03（Asia/Shanghai）
**对应上游**：3 个 release 全部资产，9 个文件，共约 698 MB

---

## 为什么备份

这条 honk 线的构建**不是从上游源码编的**，而是「自建 ImageBuilder + 自编译内核 + 全量 apk」三件套拼起来的。三件都在 `immortalwrt-artifacts` 的三个 release 里，workflow 每一步都用 sha256 钉死：

| 上游 release | 拿它干什么 | 丢了会怎样 |
|---|---|---|
| `v25.12.2-ib-x86-64` | ImageBuilder 本体（内核带 `CONFIG_DYNAMIC_FTRACE` 等五项） | 退回官方 IB → 内核没有 ftrace → honk 起不来，固件能开机但代理是死的 |
| `v25.12.2-pkg-x86-64` | 1,302 个 apk（含 1,199 个 kmod），内核 hash `71cc20e3` 配套 | 官方 kmods 源只有 `0413601b` 那一个 hash，kmod 全取不到 → `make image` 直接 Error 99 |
| `v25.12.2-fw-x86-64` | 上一次成功的固件产物 | 失去可比对的基线，出问题无法二分 |

上游仓库是**自己名下、可随时被删**的仓库，且 release 资产可以被静默替换（同名覆盖不报错）。workflow 里的 sha256 断言只会在**构建时**红，一旦某天资产被换掉而没人跑构建，问题会一直藏着。

所以这里留一份完整副本，目的只有一个：**上游没了或被改了，还能照原样重建，而且知道原来长什么样。**

---

## 目录结构

按项目类型分文件夹：

```
backups/immortalwrt-artifacts/
├── imagebuilder/          ImageBuilder（对应 v25.12.2-ib-x86-64）
│   ├── immortalwrt-imagebuilder-25.12.2-x86-64.Linux-x86_64.tar.zst
│   └── sha256sums
├── packages-x86_64/       全量 apk 产物（对应 v25.12.2-pkg-x86-64）
│   ├── packages-x86_64-25.12.2.tar.zst.part-00 … part-04
│   └── sha256sums
└── firmware-x86_64/       固件产物（对应 v25.12.2-fw-x86-64）
    ├── immortalwrt-25.12.2-x86-64-generic-kernel.bin
    ├── immortalwrt-25.12.2-x86-64-generic-squashfs-combined-efi.img.gz
    ├── immortalwrt-25.12.2-x86-64-generic-squashfs-combined.img.gz
    ├── immortalwrt-25.12.2-x86-64-generic-squashfs-rootfs.img.gz
    └── sha256sums
```

---

## 分片说明

GitHub 单个文件硬上限 **100 MiB**（104,857,600 B）。`packages-x86_64-25.12.2.tar.zst` 有 326,442,366 B，只能拆：

| 分片 | 大小 |
|---|---|
| part-00 ~ part-03 | 75,000,000 B × 4 |
| part-04 | 26,442,366 B |
| 合计 | 326,442,366 B |

**合并**：

```sh
cat packages-x86_64-25.12.2.tar.zst.part-0* > packages-x86_64-25.12.2.tar.zst
```

合并后 sha256 必须是 `4ad8465468b66852926178b373be53add7c2517fb351c1575b00ede63dd75cfe`。

固件里两个最大的 `combined-efi.img.gz`（103,353,556 B）和 `combined.img.gz`（103,148,480 B）都在 100 MiB 以内，不用拆。

---

## 校验值

| 文件 | 字节 | sha256 |
|---|---|---|
| immortalwrt-imagebuilder-25.12.2-x86-64.Linux-x86_64.tar.zst | 62,808,601 | `18b62f95ad687920a28b3a07eeb79c72cfd25147973074e979a73a718e4767d7` |
| packages-x86_64-25.12.2.tar.zst | 326,442,366 | `4ad8465468b66852926178b373be53add7c2517fb351c1575b00ede63dd75cfe` |
| immortalwrt-25.12.2-x86-64-generic-kernel.bin | 7,828,480 | `eb7477a5a63b023a62face3b045769409eac079b19c4d8bf2741bdcf395feaae` |
| immortalwrt-25.12.2-x86-64-generic-squashfs-combined-efi.img.gz | 103,353,556 | `e5557bbbd49c7e8d6cb4a885ed95a547c1426504f7780783391fce5d5341fd2b` |
| immortalwrt-25.12.2-x86-64-generic-squashfs-combined.img.gz | 103,148,480 | `c2e246fd5930168b5b99dad648eadb3beecdcfcb293057453852f235993b77ce` |
| immortalwrt-25.12.2-x86-64-generic-squashfs-rootfs.img.gz | 94,906,162 | `3f650b421e674dd336569d460bc8622a2c1ec69094618860e45af14a9ce8312c` |
| sha256sums（三份内容相同） | 145,756 | `5b03aeed85308fdd3a7ec4f98064fe02687707400032ff2143beca467cdab796` |

上游三个 release 的 `sha256sums` 是**同一个文件**，所以三个目录各放一份，不是重复劳动。

---

## 实测校验记录（2026-11-03）

| 项目 | 结果 |
|---|---|
| pkg 5 分片合并 | `4ad8465468b66852…` ✅ 与上游 digest 一致 |
| kernel.bin | `eb7477a5a63b023a…` ✅ |
| combined-efi.img.gz | `e5557bbbd49c7e8d…` ✅ |
| combined.img.gz | `c2e246fd5930168b…` ✅ |
| rootfs.img.gz | `3f650b421e674dd3…` ✅ |
| sha256sums（原暂存） | ✗ 不符，已用上游正确版本替换 |

---

## 不在备份范围内

`/tmp/rel/fw/` 里那个 `immortalwrt-25.12.2-x86-64-generic-image-efi.iso`（312,033,280 B）**不在** `immortalwrt-artifacts` 的任何一个 release 里，属于范围外，未备份。
