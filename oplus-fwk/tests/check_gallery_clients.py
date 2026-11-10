#!/usr/bin/env python3
"""Compile and check the actual stock-app ABI, including the reference's field-width defect."""
from pathlib import Path
import argparse
import subprocess
import tempfile
p=argparse.ArgumentParser();p.add_argument('--rom-root',required=True,type=Path);a=p.parse_args()
source=Path(__file__).resolve().parents[1]/'src'
files=['android/app/OplusWhiteListManager.java','com/oplus/util/OplusChangeTextUtil.java','android/common/IOplusCommonFeature.java','android/common/IOplusCommonFactory.java',
       'android/common/OplusFeatureList.java','android/common/OplusFrameworkFactory.java',
       'com/oplus/app/OPlusAccessControlManager.java','com/oplus/content/OplusFeatureConfigManager.java',
       'android/content/res/OplusBaseConfiguration.java','oplus/content/res/OplusExtraConfiguration.java']
with tempfile.TemporaryDirectory(prefix='guacamole-gallery-abi-') as tmp:
    tmp=Path(tmp)
    test=tmp/'ContractCheck.java'
    test.write_text('''import com.oplus.app.OPlusAccessControlManager;
import com.oplus.content.OplusFeatureConfigManager;
import android.content.res.OplusBaseConfiguration;
import oplus.content.res.OplusExtraConfiguration;
public class ContractCheck {public static void main(String[] args)throws Exception {
 var lists=new android.app.OplusWhiteListManager(null);
 for(String method:new String[]{"getGlobalWhiteList","getGlobalProcessWhiteList"})
  if(lists.getClass().getMethod(method).getReturnType()!=java.util.ArrayList.class)throw new AssertionError("Stock DEX return descriptor: "+method);
 if(lists.getClass().getMethod("getStageProtectListFromPkg",String.class,int.class).getReturnType()!=java.util.ArrayList.class)throw new AssertionError("Stage-protect return descriptor");
 lists.addStageProtectInfo("com.oneplus.gallery",5000L);
 if(!lists.getStageProtectListFromPkg("com.oneplus.gallery",0).isEmpty())throw new AssertionError("No absent OEM backend protection may be invented");
 var first=lists.getGlobalWhiteList();first.add("caller-mutated");
 if(!lists.getGlobalWhiteList().isEmpty()||!lists.getGlobalProcessWhiteList().isEmpty())throw new AssertionError("Caller cannot mutate shared backend state");
 lists.removeStageProtectInfo("com.oneplus.gallery");
 var feature=new android.common.IOplusCommonFeature(){};
 if(android.common.OplusFrameworkFactory.getInstance().getFeature(feature)!=feature)throw new AssertionError("Missing vendor feature must preserve the supplied SDK default");
 try{android.common.OplusFrameworkFactory.getInstance().getFeature(null);throw new AssertionError("null feature accepted");}catch(IllegalArgumentException expected){}
 if(!Float.isFinite(com.oplus.util.OplusChangeTextUtil.getSuitableFontSize(16f,0f,3)))throw new AssertionError("invalid font scale");
 if(com.oplus.util.OplusChangeTextUtil.getSuitableFontSize(16f,1f,3)!=16f)throw new AssertionError("normal-scale editor text");
 if(com.oplus.util.OplusChangeTextUtil.getSuitableFontSize(32f,2f,3)!=20f)throw new AssertionError("stock large-font editor cap");
 var lock=OPlusAccessControlManager.getInstance();
 if(lock.isEncryptedPackage("com.oneplus.gallery",-2)||lock.isEncryptPass("com.oneplus.gallery",-2))throw new AssertionError("Must not invent a lock or authentication result");
 if(OPlusAccessControlManager.USER_CURRENT!=-2)throw new AssertionError("Current-user ABI");
 if(OplusFeatureConfigManager.getInstance().hasFeatureIPC("not.installed"))throw new AssertionError("Absent feature reported present");
 if(OplusBaseConfiguration.class.isInstance(new Object()))throw new AssertionError("Unrelated configuration must take the default font path");
 for(String field:new String[]{"mThemeChangedFlags","mMaterialColor"})if(OplusExtraConfiguration.class.getField(field).getType()!=long.class)throw new AssertionError(field+" must be long");
 for(String field:new String[]{"mFlipFont","mFontVariationSettings","mUserId"})if(OplusExtraConfiguration.class.getField(field).getType()!=int.class)throw new AssertionError(field+" must be int");
 System.out.println("PASS stock gallery font/theme ABI, feature query and lock semantics");
}}''')
    cp=a.rom_root/'out/soong/.intermediates/frameworks/base/framework/android_common/turbine-combined/framework.jar'
    subprocess.run([str(a.rom_root/'prebuilts/jdk/jdk21/linux-x86/bin/javac'),'-J-Xmx128m','-proc:none','-cp',str(cp),'-d',str(tmp),*[str(source/f) for f in files],str(test)],check=True)
    subprocess.run([str(a.rom_root/'prebuilts/jdk/jdk21/linux-x86/bin/java'),'-Xmx48m','-cp',str(tmp),'ContractCheck'],check=True)
