/*
 * Copyright (C) 2024 The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

package android.common;

public class OplusFrameworkFactory implements IOplusCommonFactory {
    public static OplusFrameworkFactory sInstance = null;

    public static OplusFrameworkFactory getInstance() {
        if (sInstance == null) {
            sInstance = new OplusFrameworkFactory();
        }
        return sInstance;
    }

    /** Return the SDK's supplied default even when its vendor index is absent. */
    @Override
    public <T extends IOplusCommonFeature> T getFeature(T def, Object... vars) {
        if (def == null) throw new IllegalArgumentException("def can not be null");
        return def;
    }

    @Override
    public boolean isValid(int index) {
        boolean validOplus =
                index < OplusFeatureList.OplusIndex.EndOplusFrameworkFactory.ordinal() &&
                index > OplusFeatureList.OplusIndex.StartOplusFrameworkFactory.ordinal();
        boolean vaildOplusOs =
                index < OplusFeatureList.OplusIndex.EndOplusOsFrameworkFactory.ordinal() &&
                index > OplusFeatureList.OplusIndex.StartOplusOsFrameworkFactory.ordinal();
        return vaildOplusOs || validOplus;
    }
}
