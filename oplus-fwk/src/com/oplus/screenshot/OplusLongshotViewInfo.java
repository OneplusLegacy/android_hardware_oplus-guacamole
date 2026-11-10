/* SPDX-License-Identifier: Apache-2.0 */
package com.oplus.screenshot;
import android.os.Parcel;
import android.os.Parcelable;
/** Exact stock single-int Parcelable contract. */
public final class OplusLongshotViewInfo implements Parcelable {
    private boolean mIsUnsupported;
    public OplusLongshotViewInfo() {}
    public OplusLongshotViewInfo(Parcel source) { readFromParcel(source); }
    public boolean isUnsupported() { return mIsUnsupported; }
    public void setUnsupported() { mIsUnsupported = true; }
    public void reset() { mIsUnsupported = false; }
    public void readFromParcel(Parcel source) { mIsUnsupported = source.readInt() == 1; }
    public void writeToParcel(Parcel dest, int flags) { dest.writeInt(mIsUnsupported ? 1 : 0); }
    public int describeContents() { return 0; }
    public static final Parcelable.Creator<OplusLongshotViewInfo> CREATOR =
            new Parcelable.Creator<OplusLongshotViewInfo>() {
        public OplusLongshotViewInfo createFromParcel(Parcel p) { return new OplusLongshotViewInfo(p); }
        public OplusLongshotViewInfo[] newArray(int size) { return new OplusLongshotViewInfo[size]; }
    };
}
