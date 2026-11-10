/* SPDX-License-Identifier: Apache-2.0 */
package android.content.res;

import oplus.content.res.OplusExtraConfiguration;

/** OEM type token. AOSP Configuration deliberately does not inherit this type. */
public abstract class OplusBaseConfiguration {
    public OplusExtraConfiguration mOplusExtraConfiguration = new OplusExtraConfiguration();
    public OplusExtraConfiguration getOplusExtraConfiguration() { return mOplusExtraConfiguration; }
}
