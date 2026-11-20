#!/bin/bash
# 解析 kenzok8/openwrt-honk 的 Release，提取 honk / luci-app-honk 两个 apk。
#
# 为什么换成 kenzok8：
#   原来是 openwrt.daeuniverse.org 的 feed 目录（beta 期临时源），五个包散在
#   feed 里，luci 界面还得另配 luci-lib-daeuniverse + i18n + vmlinux-btf-builtin
#   哨兵。kenzok8 这套把 doona 面板直接打进 luci-app-honk，总共只有两件，
#   他的 DEPENDS 也不绑 vmlinux-btf-builtin —— doona 缺件由 control.sh 启动时
#   自己判，缺 BTF 也由 control.sh 报错，不再需要占位包维持依赖链。
#
# 架构映射：kenzok8 按 ARCH_PACKAGES 全名出包，正好与我们的三个目标对齐
#   x86_64             -> x86_64
#   aarch64_generic    -> aarch64_generic
#   aarch64_cortex-a53 -> aarch64_cortex-a53
# （另有 aarch64_cortex-a72 / aarch64_cortex-a76 / arm_cortex-a7_neon-vfpv4
#   / arm_cortex-a9，本 workflow 不用）
set -euo pipefail

REPO="${HONK_REPO:-kenzok8/openwrt-honk}"
TAG="${HONK_TAG:-}"
ENVF="${GITHUB_ENV:-/dev/stdout}"

fetch() {
    if command -v curl >/dev/null 2>&1; then
        curl -sfL --retry 3 --retry-delay 2 -H 'Accept: application/vnd.github+json' "$1"
    else
        wget -qO- --tries=3 --header='Accept: application/vnd.github+json' "$1"
    fi
}

if [ -n "$TAG" ]; then
    API="https://api.github.com/repos/$REPO/releases/tags/$TAG"
else
    API="https://api.github.com/repos/$REPO/releases/latest"
fi

echo "=== 解析 Release: $API ==="
json="$(fetch "$API")" || json=""
if [ -z "$json" ]; then
    echo "::error::取不到 $REPO 的 release 清单（网络不通或 tag 不存在）"
    exit 1
fi

# 从 release JSON 里挑 <pkg>-*<arch>.apk，取版本号最大的一个。
# 前缀用 "/${pkg}-[0-9]"，luci-app-honk 不会误命中 honk。
pick() {
    local pkg="$1" arch="$2"
    printf '%s\n' "$json" \
        | grep -oE '"https://[^"]*\.apk"' | tr -d '"' \
        | grep -E "/${pkg}-[0-9][^/]*-${arch}\.apk$" \
        | sort -V | tail -n 1 || :
}

emit() {
    local key="$1" url="$2"
    if [ -z "$url" ]; then
        echo "::error::$key 取不到对应 apk"
        exit 1
    fi
    echo "  ${key} = $(basename "$url")"
    echo "${key}=${url}" >> "$ENVF"
}

HONK_X86="$(pick honk x86_64)"
emit X86_HONK_URL          "$HONK_X86"
emit X86_LUCI_APP_HONK_URL "$(pick luci-app-honk x86_64)"

emit ARM_GENERIC_HONK_URL          "$(pick honk aarch64_generic)"
emit ARM_GENERIC_LUCI_APP_HONK_URL "$(pick luci-app-honk aarch64_generic)"

emit ARM_A53_HONK_URL              "$(pick honk aarch64_cortex-a53)"
emit ARM_A53_LUCI_APP_HONK_URL     "$(pick luci-app-honk aarch64_cortex-a53)"

VERSION="$(basename "$HONK_X86" | sed -e 's/^honk-//' -e 's/-x86_64\.apk$//')"
echo "VERSION=$VERSION" >> "$ENVF"

echo ""
echo "=== 解析完成 ==="
echo "honk 版本 : $VERSION"
echo "x86 honk  : $(basename "$HONK_X86")"
