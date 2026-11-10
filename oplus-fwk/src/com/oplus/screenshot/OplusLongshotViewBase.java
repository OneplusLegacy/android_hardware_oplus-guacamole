/* SPDX-License-Identifier: Apache-2.0 */
package com.oplus.screenshot;
import android.content.Context;
public interface OplusLongshotViewBase {
    boolean canLongScroll();
    int computeLongScrollExtent();
    int computeLongScrollOffset();
    int computeLongScrollRange();
    boolean findViewsLongshotInfo(OplusLongshotViewInfo info);
    Context getContext();
    boolean isLongshotVisibleToUser();
}
