#
# Copyright (C) 2022-2024 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

SEPOLICY_PLATFORM := $(subst device/qcom/sepolicy_vndr/,,$(SEPOLICY_PATH))

BOARD_VENDOR_SEPOLICY_DIRS += \
    hardware/oplus-guacamole/sepolicy/qti/vendor \
    hardware/oplus-guacamole/sepolicy/qti/vendor/$(SEPOLICY_PLATFORM)

SYSTEM_EXT_PRIVATE_SEPOLICY_DIRS += \
    hardware/oplus-guacamole/sepolicy/qti/private \
    hardware/oplus-guacamole/sepolicy/qti/private/$(SEPOLICY_PLATFORM)

SYSTEM_EXT_PUBLIC_SEPOLICY_DIRS += \
    hardware/oplus-guacamole/sepolicy/qti/public \
    hardware/oplus-guacamole/sepolicy/qti/public/$(SEPOLICY_PLATFORM)

ifneq ($(SEPOLICY_PLATFORM), legacy-um)
BOARD_VENDOR_SEPOLICY_DIRS += \
    hardware/oplus-guacamole/sepolicy/qti/vendor/common-um

SYSTEM_EXT_PRIVATE_SEPOLICY_DIRS += \
    hardware/oplus-guacamole/sepolicy/qti/private/common-um

SYSTEM_EXT_PUBLIC_SEPOLICY_DIRS += \
    hardware/oplus-guacamole/sepolicy/qti/public/common-um
endif

include device/lineage/sepolicy/libperfmgr/sepolicy.mk
