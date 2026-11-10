/*
 * Copyright (C) 2024 The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

package com.oplus.content;

import java.util.List;

public class OplusFeatureConfigManager {
    public static OplusFeatureConfigManager sInstance = null;

    public static OplusFeatureConfigManager getInstance() {
        if (sInstance == null) {
            sInstance = new OplusFeatureConfigManager();
        }
        return sInstance;
    }

    public boolean hasFeature(String featureName) {
        return false;
    }

    /** No OEM feature service is installed; use the same local capability result. */
    public boolean hasFeatureIPC(String featureName) {
        return hasFeature(featureName);
    }

    public interface OnFeatureObserver {
        default void onFeatureUpdate(List<String> features) {}
    }
}
