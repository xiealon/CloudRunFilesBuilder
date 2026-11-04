# 许可（分两部分）

**Copyright (c) 2026-11-05 xiealon**

> 最后更新：2026-11-05 06:05（Asia/Shanghai）

本目录里的东西不是同一种许可，分开说。

## 一、构建产物 —— GPL-2.0

下列文件是 ImmortalWrt 的构建产物，遵循上游 **GNU General Public License v2.0**：

- ImageBuilder（`immortalwrt-imagebuilder-*.tar.zst`，内含 6.12.103 内核）
- apk 集合（`packages-x86_64-*.tar.zst`，1,307 个 apk，含 1,204 个 kmod）
- 固件镜像（`*-generic-kernel.bin`、`*-squashfs-*.img.gz`）

全文见同目录 **`LICENSE-GPL-2.0`**（18,092 B）。

上游：`immortalwrt/immortalwrt`，其 `COPYING` 写明 `SPDX-License-Identifier: GPL-2.0`。

## 二、整理与说明 —— MIT

下列内容由本仓库编写，适用 **MIT**：

- `README.md`（本文件）
- `sha256sums`、`SHA256SUMS`、`packages-x86_64-*.tar.zst.sha256`（校验文件）
- 本 `LICENSE.md` 与 `LICENSE`
- 拆分、归档的组织方式

全文见同目录 **`LICENSE`**。

---

## MIT 全文

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
