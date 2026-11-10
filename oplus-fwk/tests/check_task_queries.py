#!/usr/bin/env python3
"""Check the real query client against a permission-filtered AOSP task service."""
from pathlib import Path
import argparse
import subprocess
import tempfile
p=argparse.ArgumentParser();p.add_argument('--rom-root',required=True,type=Path);a=p.parse_args()
fakes={
'android/content/ComponentName.java': 'package android.content; public class ComponentName {final String name;public ComponentName(String n){name=n;}public String getPackageName(){return name;}}',
'android/content/pm/ActivityInfo.java': 'package android.content.pm; public class ActivityInfo {public Object applicationInfo;}',
'android/app/ActivityManager.java': '''package android.app; public class ActivityManager {public static class RunningTaskInfo {
public int taskId,displayId,userId;public android.content.ComponentName topActivity,baseActivity;
public android.content.pm.ActivityInfo topActivityInfo;
public Config configuration=new Config();
public static class Config {public Window windowConfiguration=new Window();public int orientation;}
public static class Window {public int getWindowingMode(){return 1;}public int getActivityType(){return 1;}public Object getBounds(){return this;}}
}}''',
'android/app/ActivityTaskManager.java': '''package android.app; import java.util.*;public class ActivityTaskManager {
public static final ActivityTaskManager INSTANCE=new ActivityTaskManager();public static int calls,max;public static boolean visible,deny;
public static List<ActivityManager.RunningTaskInfo> tasks=new ArrayList<>();
public static ActivityTaskManager getInstance(){return INSTANCE;}
public List<ActivityManager.RunningTaskInfo> getTasks(int n,boolean v){calls++;max=n;visible=v;if(deny)throw new SecurityException();return tasks;}}
''',
'com/oplus/app/OplusAppInfo.java': '''package com.oplus.app; public class OplusAppInfo {
public int taskId,displayId,userId,windowingMode,activityType,orientation;public Object appInfo;
public android.content.ComponentName topActivity;public Bounds appBounds=new Bounds();
public static class Bounds{public void set(Object b){}}
}''',
'QueryCheck.java': '''import android.app.*;import android.content.*;public class QueryCheck {
public static void main(String[] args){
var client=new OplusActivityManager();if(ActivityTaskManager.calls!=0)throw new AssertionError("constructor IPC");
var task=new ActivityManager.RunningTaskInfo();task.taskId=42;task.displayId=0;task.userId=10;
task.topActivity=new ComponentName("com.oneplus.gallery");task.baseActivity=task.topActivity;
ActivityTaskManager.tasks.add(task);
var infos=client.getAllTopAppInfos();if(infos.size()!=1||infos.get(0).taskId!=42||infos.get(0).userId!=10)throw new AssertionError("task metadata");
if(!ActivityTaskManager.visible)throw new AssertionError("visible query flag lost");
if(client.getTopActivityComponentName()!=task.topActivity)throw new AssertionError("top activity");
if(client.getTaskPkgList(42).size()!=1)throw new AssertionError("duplicate package");
OplusActivityManager.getFilteredTasks(10000,false);if(ActivityTaskManager.max!=128)throw new AssertionError("unbounded task request");
int calls=ActivityTaskManager.calls;OplusActivityManager.getFilteredTasks(0,false);if(calls!=ActivityTaskManager.calls)throw new AssertionError("invalid request issued");
ActivityTaskManager.deny=true;if(!client.getAllTopAppInfos().isEmpty()||client.getTopActivityComponentName()!=null)throw new AssertionError("must not invent private task state");
System.out.println("PASS constructor without IPC, typed task queries, bounded requests and permission denial");
}}
'''}
with tempfile.TemporaryDirectory(prefix='guacamole-task-query-') as temp:
    temp=Path(temp)
    for relative,text in fakes.items():
        target=temp/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
    source=Path(__file__).resolve().parents[1]/'src/android/app/OplusActivityManager.java'
    subprocess.run([str(a.rom_root/'prebuilts/jdk/jdk21/linux-x86/bin/javac'),'-J-Xmx128m','-proc:none','-d',str(temp),str(source),*[str(s) for s in temp.rglob('*.java')]],check=True)
    subprocess.run([str(a.rom_root/'prebuilts/jdk/jdk21/linux-x86/bin/java'),'-Xmx48m','-cp',str(temp),'QueryCheck'],check=True)
