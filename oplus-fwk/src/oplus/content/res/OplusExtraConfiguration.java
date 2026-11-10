/* SPDX-License-Identifier: Apache-2.0 */
package oplus.content.res;

/** Fields read by the stock gallery's optional OEM font/theme path. */
public final class OplusExtraConfiguration {
    public int mFont;
    public int mFlipFont = -1;
    public int mFontVariationSettings;
    public int mUserId;
    public long mMaterialColor;
    // These are longs in the stock APK, unlike the older reference shim.
    public long mThemeChangedFlags;
}
