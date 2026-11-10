#!/usr/bin/env python3
"""Exercise the real registry hook and client without starting an Android build."""
import argparse
from pathlib import Path
import subprocess
import tempfile

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--rom-root', type=Path, required=True)
parser.add_argument('--framework-source', type=Path)
args=parser.parse_args()
source=Path(__file__).resolve().parents[1]/'src'
registry=args.framework_source or args.rom_root/'frameworks/base/core/java/android/app/SystemServiceRegistry.java'
text=registry.read_text()
start=text.index('    @SuppressWarnings("unchecked")\n    private static void registerOplusHapticsWrapper()')
opening=text.index('{',start)
depth=1; end=opening+1
while depth:
    if text[end]=='{': depth+=1
    elif text[end]=='}': depth-=1
    end+=1
helper=text[start:end].replace('SystemServiceRegistry.class', 'RegistryCheck.class')
stubs={
'android/content/Context.java': '''package android.content;
public class Context {
 public Object getSystemService(String name) {
  if(name.equals("vibrator")) return new android.os.Vibrator();
  if(name.equals("vibrator_manager")) return new android.os.VibratorManager();
  return null;
 }
}''',
'android/app/ContextImpl.java': '''package android.app; public class ContextImpl {
 public android.content.Context getOuterContext(){return new android.content.Context();}
}''',
'android/os/Vibrator.java': '''package android.os; public class Vibrator {
 public static int calls; public void vibrate(VibrationEffect effect){calls++;}
}''',
'android/os/VibrationEffect.java': '''package android.os; public class VibrationEffect {
 public static VibrationEffect createPredefined(int effect){return new VibrationEffect();}
}''',
'android/os/VibratorManager.java': 'package android.os; public class VibratorManager {}',
'android/os/VibrationAttributes.java': 'package android.os; public class VibrationAttributes {}',
'android/os/IInterface.java': 'package android.os; public interface IInterface { IBinder asBinder(); }',
'android/os/IBinder.java': 'package android.os; public interface IBinder {}',
'android/os/RemoteException.java': 'package android.os; public class RemoteException extends Exception {}',
'android/os/Parcel.java': 'package android.os; public class Parcel {}',
'android/os/Parcelable.java': '''package android.os; public interface Parcelable {
 interface Creator<T> {T createFromParcel(Parcel p); T[] newArray(int count);}
}''',
'android/util/Slog.java': '''package android.util; public class Slog {
 public static int d(String tag,String message){return 0;}
 public static int w(String tag,String message,Throwable error){throw new AssertionError(error);}
}''',
}
fixture='''package android.app;
import android.content.Context;
import android.util.Slog;
public class RegistryCheck {
 static final String TAG="RegistryCheck";
 static Object registered; static CachedServiceFetcher<?> fetcher;
 abstract static class CachedServiceFetcher<T> { abstract T createService(ContextImpl context); }
 static <T> void registerService(String name,Class<T> type,CachedServiceFetcher<T> f) {
  if(!name.equals("linearmotor") || !type.getName().equals("com.oplus.os.LinearmotorVibrator"))
   throw new AssertionError("Wrong registered service identity");
  registered=type; fetcher=f;
 }
HELPER
 public static void main(String[] argv) throws Exception {
  registerOplusHapticsWrapper();
  if(argv.length>0) {
   if(registered!=null)throw new AssertionError("Unexpected service without optional boot jar");
   System.out.println("PASS: products without the optional client remain unchanged"); return;
  }
  if(fetcher==null)throw new AssertionError("Missing linearmotor registration");
  Object client=fetcher.createService(new ContextImpl());
  Class<?> effect=Class.forName("com.oplus.os.WaveformEffect");
  client.getClass().getMethod("vibrate",effect).invoke(client,new Object[]{null});
  if(android.os.Vibrator.calls!=1)throw new AssertionError("Haptics did not reach AOSP Vibrator");
  System.out.println("PASS: registered service returns the concrete client and delegates haptics");
 }
}'''.replace('HELPER',helper)
with tempfile.TemporaryDirectory(prefix='guacamole-haptics-') as temporary:
    work=Path(temporary)
    for name,body in stubs.items():
        path=work/'fixtures'/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(body)
    check=work/'fixtures/android/app/RegistryCheck.java';check.write_text(fixture)
    java=args.rom_root/'prebuilts/jdk/jdk21/linux-x86/bin'
    fixture_classes=work/'fixture-classes';fixture_classes.mkdir()
    subprocess.run([str(java/'javac'),'-J-Xmx96m','-d',str(fixture_classes),
                    *map(str,(work/'fixtures').rglob('*.java'))],check=True)
    production=work/'production';production.mkdir()
    headers=args.rom_root/'out/soong/.intermediates/frameworks/base/framework/android_common/turbine-combined/framework.jar'
    subprocess.run([str(java/'javac'),'-J-Xmx192m','-proc:none','-cp',str(headers),'-d',str(production),
        *[str(source/'com/oplus/os'/name) for name in ['LinearmotorVibrator.java','ILinearmotorVibratorService.java','WaveformEffect.java']]],check=True)
    subprocess.run([str(java/'java'),'-Xmx48m','-cp',str(fixture_classes),'android.app.RegistryCheck','absent'],check=True)
    subprocess.run([str(java/'java'),'-Xmx48m','-cp',str(fixture_classes)+':'+str(production),'android.app.RegistryCheck'],check=True)
