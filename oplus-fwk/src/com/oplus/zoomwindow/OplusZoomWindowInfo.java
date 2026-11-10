/* SPDX-License-Identifier: Apache-2.0 */
package com.oplus.zoomwindow;

import android.graphics.Rect;
import android.os.Bundle;
import android.os.Parcel;
import android.os.Parcelable;

/** OxygenOS 12 parcel shape used by the Gallery addon, without a vendor service. */
public final class OplusZoomWindowInfo implements Parcelable {
    public int rotation, systemRotation, lockUserId, zoomUserId, lastExitMethod;
    public int inputMethodType, cvActionFlag, windowType, sideOfFloatHandle;
    public boolean windowShown, inputShow;
    public String lockPkg, zoomPkg, cpnName;
    public Rect zoomRect = new Rect();
    public Bundle extension = new Bundle();
    public float leftScaleOfFloatHandleCenter, rightScaleOfFloatHandleCenter;
    public OplusZoomWindowInfo() {}
    public OplusZoomWindowInfo(Parcel in) { readFromParcel(in); }
    public OplusZoomWindowInfo(OplusZoomWindowInfo other) {
        if (other == null) return;
        Parcel parcel = Parcel.obtain();
        try { other.writeToParcel(parcel, 0); parcel.setDataPosition(0); readFromParcel(parcel); }
        finally { parcel.recycle(); }
    }
    public void readFromParcel(Parcel in) {
        rotation=in.readInt(); systemRotation=in.readInt(); windowShown=in.readByte()!=0;
        lockPkg=in.readString(); zoomRect=in.readParcelable(Rect.class.getClassLoader(), Rect.class);
        zoomPkg=in.readString(); lockUserId=in.readInt(); zoomUserId=in.readInt();
        inputShow=in.readByte()!=0; cpnName=in.readString(); lastExitMethod=in.readInt();
        inputMethodType=in.readInt(); extension=in.readBundle(Bundle.class.getClassLoader());
        cvActionFlag=in.readInt(); windowType=in.readInt();
        leftScaleOfFloatHandleCenter=in.readFloat(); rightScaleOfFloatHandleCenter=in.readFloat();
        sideOfFloatHandle=in.readInt();
    }
    @Override public void writeToParcel(Parcel out, int flags) {
        out.writeInt(rotation); out.writeInt(systemRotation); out.writeByte((byte)(windowShown?1:0));
        out.writeString(lockPkg); out.writeParcelable(zoomRect, flags); out.writeString(zoomPkg);
        out.writeInt(lockUserId); out.writeInt(zoomUserId); out.writeByte((byte)(inputShow?1:0));
        out.writeString(cpnName); out.writeInt(lastExitMethod); out.writeInt(inputMethodType);
        out.writeBundle(extension); out.writeInt(cvActionFlag); out.writeInt(windowType);
        out.writeFloat(leftScaleOfFloatHandleCenter); out.writeFloat(rightScaleOfFloatHandleCenter);
        out.writeInt(sideOfFloatHandle);
    }
    @Override public int describeContents() { return 0; }
    public static final Creator<OplusZoomWindowInfo> CREATOR = new Creator<>() {
        public OplusZoomWindowInfo createFromParcel(Parcel in) { return new OplusZoomWindowInfo(in); }
        public OplusZoomWindowInfo[] newArray(int count) { return new OplusZoomWindowInfo[count]; }
    };
}
