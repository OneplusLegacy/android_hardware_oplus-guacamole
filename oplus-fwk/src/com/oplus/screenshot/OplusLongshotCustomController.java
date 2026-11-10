/* SPDX-License-Identifier: Apache-2.0 */
package com.oplus.screenshot;
/** Gallery view hook only: this ROM has no OEM longshot service. */
public class OplusLongshotCustomController {
    public OplusLongshotCustomController(OplusLongshotViewBase view, String source) {}
    public boolean findInfo(OplusLongshotViewInfo info) {
        if (info != null) info.setUnsupported();
        return false;
    }
    public void onLongScroll() {}
}
