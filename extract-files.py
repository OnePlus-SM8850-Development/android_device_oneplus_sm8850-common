#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/oneplus/sm8850-common',
    'hardware/oplus',
    'hardware/qcom-caf/sm8850',
    'hardware/qcom-caf/wlan',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'libolc_vnd',
        'libosensenativeproxy_client',
        'libPanelChaplin',
        'vendor.qti.ImsRtpService-V2-ndk',
        'vendor.qti.diaghal-V1-ndk',
        'vendor.qti.hardware.dpmaidlservice-V1-ndk',
        'vendor.qti.hardware.wifidisplaysession_aidl-V1-ndk',
        'vendor.qti.qccsyshal_aidl-V1-ndk',
        'vendor.qti.qccvndhal_aidl-V1-ndk',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    'odm/bin/hw/vendor.oplus.hardware.biometrics.fingerprint@2.1-service_uff': blob_fixup()
        .add_needed('libshims_aidl_fingerprint_v3.oplus.so'),
    (
        'odm/bin/hw/vendor-oplus-hardware-touch-V2-hbp5-service',
        'odm/bin/hw/vendor.oplus.hardware.biometrics.fingerprint@2.1-service_uff',
        'odm/bin/touchDaemon',
        'odm/lib64/libdisplayfossfeature_nature.so',
        'odm/lib64/libstc_color_feature.so',
        'vendor/bin/hw/audiohalservice.qti',
        'vendor/bin/hw/vendor.qti.hardware.display.composer-service',
        'vendor/bin/poweropt-service',
        'vendor/bin/qsap_mpamsvc',
        'vendor/bin/qvrdatauploader',
        'vendor/lib64/hw/libaudioeffecthal.qti.so',
        'vendor/lib64/libaodoptfeature.so',
        'vendor/lib64/libapengine.so',
        'vendor/lib64/libcamerapoweroptfeature.so',
        'vendor/lib64/libgamepoweroptfeature.so',
        'vendor/lib64/liblearningmodule.so',
        'vendor/lib64/liboffscreenpoweroptfeature.so',
        'vendor/lib64/libpowercallback.so',
        'vendor/lib64/libpowercore.so',
        'vendor/lib64/libpsmoptfeature.so',
        'vendor/lib64/libstandbyfeature.so',
        'vendor/lib64/libvideooptfeature.so',
        'vendor/lib64/soundfx/libquasar.so',
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v36.so'),
    'odm/etc/gps.conf': blob_fixup()
        .binary_regex_replace(b'com.oplus.locationproxy', b'com.google.android.carrierlocation')
        .binary_regex_replace(b'DEBUG_LEVEL = 3', b'DEBUG_LEVEL = 2'),
    'odm/etc/init/init.network.rc': blob_fixup()
        .regex_replace(r'/\* (Huo\.Chen@SYSTEM\.RF, 2024/09/06, Add for ICC) \*/', r'# \1'),
    'product/etc/sysconfig/com.android.hotwordenrollment.common.util.xml': blob_fixup()
        .regex_replace('/my_product', '/product'),
    'system/framework/WfdCommon.jar': blob_fixup()
        .apktool_patch('blob-patches/WfdCommon.patch'),
    'system_ext/bin/horae': blob_fixup()
        .replace_needed('libprotobuf-cpp-lite.so', 'libprotobuf-cpp-lite-21.12.so'),
    (
        'system_ext/etc/seccomp_policy/tcmd.policy',
        'vendor/etc/seccomp_policy/qsap_qapeservice.policy',
        'vendor/etc/seccomp_policy/syshealthmon.policy'
    ): blob_fixup()
        .add_line_if_missing('lseek: 1'),
    'system_ext/lib64/libwfdservice.so': blob_fixup()
        .replace_needed('android.media.audio.common.types-V4-cpp.so', 'android.media.audio.common.types-V5-cpp.so'),
    'vendor/bin/vendor_modprobe.sh': blob_fixup()
        .regex_replace(r'\n.*OPLUS_FEATURE_WIFI_FTM[\s\S]*?OPLUS_FEATURE_WIFI_FTM.*\n', ''),
    (
        'vendor/bin/hw/vendor.qti.media.c2@1.0-service',
        'vendor/bin/hw/vendor.qti.media.c2audio@1.0-service',
    ): blob_fixup()
        .replace_needed('android.hardware.media.c2-V1-ndk.so', 'android.hardware.media.c2-V2-ndk.so'),
    'vendor/etc/perf/perfboostsconfig.xml': blob_fixup()
        .regex_replace(r'Enable="false"', r'Enable="true"'),
    (
        'vendor/etc/media_codecs_canoe_sku3.xml',
        'vendor/etc/media_codecs_canoe_v2.xml',
    ): blob_fixup()
        .regex_replace('.*media_codecs_(google_audio|google_c2|google_telephony|google_video|vendor_audio).*\n', ''),
    'vendor/lib64/libaudioserviceexampleimpl.so': blob_fixup()
        .add_needed('libaudioutils_shim.so')
        .add_needed('libbluetooth_audio_session_aidl_shim.so'),
    (
        'vendor/lib64/libcwb_qcom_aidl.so',
        'vendor/lib64/libhwcsensor.so',
    ): blob_fixup()
        .replace_needed('vendor.qti.hardware.display.config-V11-ndk.so', 'vendor.qti.hardware.display.config-V13-ndk.so'),
    'vendor/lib64/libqcodec2_core.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    'vendor/usr/keylayout/gpio-keys.kl': blob_fixup()
        .add_line_if_missing('key 735   ASSIST'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm8850-common',
    'oneplus',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)
module.add_proprietary_file('proprietary-files-phone.txt').add_copy_files_guard(
    'TARGET_IS_TABLET', 'true', invert=True
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
