/* SPDX-License-Identifier: Apache-2.0 */
package com.oplus.app;

import android.os.UserHandle;

/** Compatibility query for the absent OEM app-lock backend. */
public final class OPlusAccessControlManager {
    public static final int USER_CURRENT = UserHandle.USER_CURRENT;
    private static final OPlusAccessControlManager INSTANCE = new OPlusAccessControlManager();
    private OPlusAccessControlManager() {}
    public static OPlusAccessControlManager getInstance() { return INSTANCE; }
    public boolean isEncryptedPackage(String packageName, int userId) { return false; }
    // Do not manufacture an authentication result for another lock backend.
    public boolean isEncryptPass(String packageName, int userId) { return false; }
}
