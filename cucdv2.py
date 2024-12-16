import os
import shutil
import subprocess
import win32com.client
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def print_progress_bar(progress, total, bar_length=50):
    percent = (progress / total) * 100
    filled_length = int(bar_length * progress // total)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    print(f"\r[{bar}] {percent:.2f}% ({progress}/{total})", end="", flush=True)

def clear_temp():
    print("\nStarting to clear temporary files. Please wait...")

    temp_dirs = [os.getenv("TEMP"), os.getenv("TMP"), os.path.join(os.getenv("SYSTEMROOT"), "Temp")]
    all_files = []
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                all_files.append(file_path)

    total_files = len(all_files)
    if total_files == 0:
        print("\nNo files to clear in Temp folders.")
        return

    error_count = 0

    for idx, file_path in enumerate(all_files):
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

            print_progress_bar(idx + 1, total_files)

        except PermissionError:
            error_count += 1
            print_progress_bar(idx + 1, total_files)
        except Exception as e:
            error_count += 1
            print_progress_bar(idx + 1, total_files)

    print("\nTemporary files cleanup completed.")
    
    if error_count > 0:
        print(f"\nProcessed {error_count} errors when deleting files. Some files were in use.")

def clear_recycle_bin():
    print("\nClearing the Recycle Bin...")
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.Run("cmd /c rd /s /q C:\\$Recycle.Bin")
        print("Recycle Bin cleared.")
    except Exception as e:
        print(f"Error clearing the Recycle Bin: {e}")

def disable_hibernation():
    print("\nDisabling hibernation...")
    try:
        subprocess.run(["powercfg", "/hibernate", "off"], check=True)
        print("Hibernation disabled.")
    except subprocess.CalledProcessError:
        print("Failed to disable hibernation.")

def clean_disk():
    print("\nRunning disk cleanup...")
    try:
        subprocess.run(["cleanmgr", "/sagerun:1"], check=True)
        print("Disk cleanup completed.")
    except subprocess.CalledProcessError:
        print("Failed to clean the disk.")

def clear_event_logs():
    print("\nClearing system logs...")
    try:
        subprocess.run(["wevtutil", "cl", "Application"], check=True)
        subprocess.run(["wevtutil", "cl", "System"], check=True)
        subprocess.run(["wevtutil", "cl", "Security"], check=True)
        print("System logs cleared.")
    except subprocess.CalledProcessError:
        print("Failed to clear system logs.")

def clear_browser_cache():
    print("\nClearing browser caches...")
    
    chrome_cache = os.path.join(os.getenv("LOCALAPPDATA"), "Google\\Chrome\\User Data\\Default\\Cache")
    edge_cache = os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft\\Edge\\User Data\\Default\\Cache")
    
    try:
        if os.path.exists(chrome_cache):
            shutil.rmtree(chrome_cache)
            print("Chrome cache cleared.")
        else:
            print("Chrome cache not found.")
        
        if os.path.exists(edge_cache):
            shutil.rmtree(edge_cache)
            print("Edge cache cleared.")
        else:
            print("Edge cache not found.")
    except Exception as e:
        print(f"Error clearing browser caches: {e}")

def clear_windows_update_cache():
    print("\nClearing Windows update cache...")
    update_cache_dir = os.path.join(os.getenv("WINDIR"), "SoftwareDistribution", "Download")
    
    try:
        if os.path.exists(update_cache_dir):
            shutil.rmtree(update_cache_dir)
            print("Windows update cache cleared.")
        else:
            print("Windows update cache not found.")
    except Exception as e:
        print(f"Error clearing Windows update cache: {e}")

def clear_installer_temp():
    print("\nClearing Windows installer temporary files...")
    temp_dirs = [os.path.join(os.getenv("WINDIR"), "Temp"), os.path.join(os.getenv("USERPROFILE"), "AppData\\Local\\Temp")]
    
    try:
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}: {e}")
        print("Windows installer temporary files cleared.")
    except Exception as e:
        print(f"Error clearing Windows installer temporary files: {e}")

def delete_old_system_restore_points():
    print("\nDeleting old system restore points...")
    try:
        subprocess.run(["vssadmin", "delete", "shadows", "/for=c:", "/oldest"], check=True)
        print("Old restore points deleted.")
    except subprocess.CalledProcessError:
        print("Failed to delete old restore points.")

def clear_prefetch():
    print("\nClearing Prefetch folder...")
    prefetch_dir = os.path.join(os.getenv("WINDIR"), "Prefetch")
    
    try:
        if os.path.exists(prefetch_dir):
            for filename in os.listdir(prefetch_dir):
                file_path = os.path.join(prefetch_dir, filename)
                try:
                    os.unlink(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
            print("Prefetch folder cleared.")
        else:
            print("Prefetch folder not found.")
    except Exception as e:
        print(f"Error clearing Prefetch folder: {e}")

def clear_windows_store_cache():
    print("\nClearing Windows Store cache...")
    try:
        subprocess.run(["wsreset.exe"], check=True)
        print("Windows Store cache cleared.")

        subprocess.run(["taskkill", "/IM", "WinStore.App.exe", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Microsoft Store automatically closed.")
    except subprocess.CalledProcessError:
        print("Failed to clear Windows Store cache.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def clear_driver_install_logs():
    print("\nClearing driver installation logs...")
    driver_log_dir = os.path.join(os.getenv("WINDIR"), "INF")
    
    try:
        for filename in os.listdir(driver_log_dir):
            if filename.endswith(".log"):
                file_path = os.path.join(driver_log_dir, filename)
                os.remove(file_path)
        print("Driver installation logs cleared.")
    except Exception as e:
        print(f"Error clearing driver installation logs: {e}")

def perform_full_cleanup():
    clear_temp()
    clear_recycle_bin()
    disable_hibernation()
    clean_disk()
    clear_event_logs()
    clear_browser_cache()
    clear_windows_update_cache()
    clear_installer_temp()
    delete_old_system_restore_points()
    clear_prefetch()
    clear_windows_store_cache()
    clear_driver_install_logs()

def main():
    while True:
        print("\nSystem Cleanup")
        print("1. Clear Temp")
        print("2. Clear Recycle Bin")
        print("3. Disable Hibernation")
        print("4. Clean Disk")
        print("5. Clear Event Logs")
        print("6. Clear Browser Cache")
        print("7. Clear Windows Update Cache")
        print("8. Clear Windows Installer Temp Files")
        print("9. Delete Old System Restore Points")
        print("10. Clear Prefetch Folder")
        print("11. Clear Windows Store Cache")
        print("12. Clear Driver Installation Logs")
        print("13. Perform Full Cleanup")
        print("0. Exit")

        choice = input("\nChoose an action (0-13): ")
        
        os.system('cls' if os.name == 'nt' else 'clear')

        if choice == "1":
            clear_temp()
        elif choice == "2":
            clear_recycle_bin()
        elif choice == "3":
            disable_hibernation()
        elif choice == "4":
            clean_disk()
        elif choice == "5":
            clear_event_logs()
        elif choice == "6":
            clear_browser_cache()
        elif choice == "7":
            clear_windows_update_cache()
        elif choice == "8":
            clear_installer_temp()
        elif choice == "9":
            delete_old_system_restore_points()
        elif choice == "10":
            clear_prefetch()
        elif choice == "11":
            clear_windows_store_cache()
        elif choice == "12":
            clear_driver_install_logs()
        elif choice == "13":
            print("\nPerforming full system cleanup...")
            perform_full_cleanup()
        elif choice == "0":
            print("\nExiting the program.")
            break
        else:
            print("\nInvalid choice. Please try again.")

run_as_admin()

if __name__ == "__main__":
    main()
