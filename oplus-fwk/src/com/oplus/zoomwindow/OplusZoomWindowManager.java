package com.oplus.zoomwindow;

public class OplusZoomWindowManager {

    public static OplusZoomWindowManager sOplusZoomWindowManager = null;

    public static OplusZoomWindowManager getInstance() {
        if (sOplusZoomWindowManager == null) {
            sOplusZoomWindowManager = new OplusZoomWindowManager();
        }
        return sOplusZoomWindowManager;
    }

    // AOSP has no OPlus floating-window service. Advertise that accurately.
    public boolean isSupportZoomWindowMode() { return false; }
    public OplusZoomWindowInfo getCurrentZoomWindowState() { return new OplusZoomWindowInfo(); }

    public boolean registerZoomWindowObserver(IOplusZoomWindowObserver observer) {
        return false;
    }

    public boolean unregisterZoomWindowObserver(IOplusZoomWindowObserver observer) {
        return false;
    }
}
