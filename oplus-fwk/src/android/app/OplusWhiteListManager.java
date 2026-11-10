/* SPDX-License-Identifier: Apache-2.0 */
package android.app;

import android.content.Context;
import java.util.ArrayList;

/** Optional OEM process-protection hints; AOSP retains its own process policy. */
public final class OplusWhiteListManager {
    public OplusWhiteListManager(Context context) {}
    public ArrayList<String> getGlobalWhiteList() { return new ArrayList<>(); }
    public ArrayList<String> getGlobalWhiteList(int type) { return new ArrayList<>(); }
    public ArrayList<String> getGlobalProcessWhiteList() { return new ArrayList<>(); }
    public ArrayList<String> getStageProtectListFromPkg(String callerPackage, int type) {
        return new ArrayList<>();
    }
    public void addStageProtectInfo(String packageName, long timeout) {}
    public void removeStageProtectInfo(String packageName) {}
}
