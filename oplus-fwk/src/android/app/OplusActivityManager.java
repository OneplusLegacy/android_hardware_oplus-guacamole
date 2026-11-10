/* SPDX-License-Identifier: Apache-2.0 */
package android.app;

import android.content.ComponentName;
import com.oplus.app.OplusAppInfo;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Task queries through AOSP's typed interface, with its caller filtering intact. */
public class OplusActivityManager {
    private static final int TASK_LIMIT = 128;
    public OplusActivityManager() {}
    public static OplusActivityManager getInstance() { return new OplusActivityManager(); }

    public static List<ActivityManager.RunningTaskInfo> getFilteredTasks(int maxNum,
            boolean filterOnlyVisibleRecents) {
        if (maxNum <= 0) return Collections.emptyList();
        try {
            return ActivityTaskManager.getInstance().getTasks(Math.min(maxNum, TASK_LIMIT),
                    filterOnlyVisibleRecents);
        } catch (SecurityException unavailableToCaller) {
            return Collections.emptyList();
        }
    }

    public List<OplusAppInfo> getAllTopAppInfos() {
        List<OplusAppInfo> result = new ArrayList<>();
        for (ActivityManager.RunningTaskInfo task : getFilteredTasks(TASK_LIMIT, true)) {
            if (task.topActivity == null) continue;
            OplusAppInfo info = new OplusAppInfo();
            info.topActivity = task.topActivity;
            info.taskId = task.taskId;
            info.displayId = task.displayId;
            info.userId = task.userId;
            info.windowingMode = task.configuration.windowConfiguration.getWindowingMode();
            info.activityType = task.configuration.windowConfiguration.getActivityType();
            info.appBounds.set(task.configuration.windowConfiguration.getBounds());
            info.orientation = task.configuration.orientation;
            if (task.topActivityInfo != null) info.appInfo = task.topActivityInfo.applicationInfo;
            result.add(info);
        }
        return result;
    }

    public ComponentName getTopActivityComponentName() {
        List<ActivityManager.RunningTaskInfo> tasks = getFilteredTasks(1, true);
        return tasks.isEmpty() ? null : tasks.get(0).topActivity;
    }

    public List<String> getTaskPkgList(int taskId) {
        for (ActivityManager.RunningTaskInfo task : getFilteredTasks(TASK_LIMIT, false)) {
            if (task.taskId != taskId) continue;
            List<String> packages = new ArrayList<>();
            if (task.baseActivity != null) packages.add(task.baseActivity.getPackageName());
            if (task.topActivity != null && !packages.contains(task.topActivity.getPackageName())) {
                packages.add(task.topActivity.getPackageName());
            }
            return packages;
        }
        return Collections.emptyList();
    }
}
