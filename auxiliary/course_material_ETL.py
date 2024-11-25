import os
import shutil
import pyfiglet
from colorama import Fore, Style
from typing import Optional

class FileProcessor:
    def __init__(self):
        self.reset_style = Style.RESET_ALL
        self.downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        self.study_material_dir = "StudyMaterial/"

    def display_banner(self) -> None:
        """Display welcome banner using pyfiglet"""
        pyfiglet.print_figlet("Welcome!", font="slant")

    def get_latest_zip_file(self) -> Optional[str]:
        """Find the latest downloaded zip file"""
        try:
            files = [f for f in os.listdir(self.downloads_dir) if f.endswith('.zip')]
            if not files:
                return None
            
            file_paths = [os.path.join(self.downloads_dir, f) for f in files]
            return max(file_paths, key=os.path.getmtime)
        except Exception as e:
            print(f"{Fore.RED}Error finding zip file: {e}{self.reset_style}")
            return None

    def unpack_file(self, path: str) -> bool:
        """Unpack the zip file to study material directory"""
        try:
            shutil.unpack_archive(path, self.study_material_dir)
            return True
        except Exception as e:
            print(f"{Fore.RED}Error unpacking file: {e}{self.reset_style}")
            return False

    def get_user_confirmation(self, prompt: str) -> bool:
        """Get user confirmation for an action"""
        return input(f"{Fore.GREEN}{prompt} (y/n): {self.reset_style}").lower() == 'y'

    def cleanup(self, zip_path: str) -> None:
        """Handle cleanup of extracted and zip files"""
        if self.get_user_confirmation("\n\tDelete the extracted files?"):
            try:
                shutil.rmtree(self.study_material_dir)
                print(f"{Fore.GREEN}\n[+] Files deleted successfully!{self.reset_style}")

                if os.path.exists(zip_path) and self.get_user_confirmation("\n\tDelete the zip file too?"):
                    os.remove(zip_path)
                    print(f"{Fore.GREEN}\n[+] Zip file also deleted successfully!{self.reset_style}")
            except Exception as e:
                print(f"{Fore.RED}\n[!] Error during cleanup: {e}{self.reset_style}")
        else:
            print(f"{Fore.RED}\n[!] Please delete the files manually{self.reset_style}")

    def process(self) -> None:
        """Main process handler"""
        self.display_banner()

        zip_path = self.get_latest_zip_file()
        if not zip_path:
            print(f"{Fore.RED}\n[!] No zip file found in Downloads folder{self.reset_style}")
            return

        print(f"{Fore.CYAN}\n[+] Found --> {Fore.YELLOW}{zip_path}")
        
        if self.get_user_confirmation("\tIs this the file you're looking for?"):
            if self.unpack_file(zip_path):
                print(f"{Fore.GREEN}\n[+] File unpacked successfully!{self.reset_style}")
                self.cleanup(zip_path)
        else:
            print(f"{Fore.RED}\n[!] Try downloading the file again in Downloads folder{self.reset_style}")

if __name__ == "__main__":
    processor = FileProcessor()
    processor.process()
