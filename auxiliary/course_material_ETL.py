import os
import shutil
import pyfiglet
from colorama import Fore, Style

r = Style.RESET_ALL

def ascii_banner():
    pyfiglet.print_figlet("Welcome!", font="slant")
    # pass

# get the latest downloaded file in downloads directory
def get_file_location():
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")

    files = [f for f in os.listdir(downloads) if f.endswith('.zip')]

    if not files:
        return "Couldn't find your file"
    file_paths = [os.path.join(downloads, f) for f in files]
    file_paths.sort(key=os.path.getmtime, reverse=True)

    return file_paths[0]

def unpack_file(path):
    #intentionally keeping for overwriting the existing files
    shutil.unpack_archive(path, "StudyMaterial/")

def handler():

    ascii_banner()

    path = get_file_location()
    print(Fore.CYAN + f"\n[+] Found --> " + Fore.YELLOW + f"{path}")
    
    user_input = str(input(Fore.GREEN + "\tIs this the file you're looking for? (y/n): " + r))
    if user_input.lower() == 'y':
        unpack_file(path=path)
        print(Fore.GREEN + "\n[+] File unpacked successfully!" + r )
    else:
        print(Fore.RED + "\n[!] Try downloading the file again in Downloads folder" + r)
        exit(0)

    # give an option to either exit or exit by deleting the downloaded directory
    user_input = str(input(Fore.RED + "\n\tDelete the downloaded file? (y/n): " + r))
    if user_input.lower() == 'y':
        shutil.rmtree('StudyMaterial/')
        print(Fore.GREEN + "\n[+] File deleted successfully!" + r)
        
        if os.path.exists(path) and str(input(Fore.RED + "\n\tDelete the zip file too? (y/n): " + r).lower()) == 'y':
            os.remove(path)
            print(Fore.GREEN + "\n[+] Zip file also deleted successfully!" + r) 
    else:
        print(Fore.RED + "\n[!] Please delete the file manually" + r)

    
handler()

