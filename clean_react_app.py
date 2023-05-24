import os
import subprocess
import shutil
import argparse
import sys


# = = = = = = = = = = FUNCTION DECLARATIONS
def copy_directory(src, dst):
    """
    Copies a directory(src) to a destination folder (dst)
    """
    # Check if source directory exists
    if not os.path.exists(src):
        print(
            f"[clean_react_app->copy_directory()]: Source directory {src} does not exist."
        )
        return

    # Check if destination directory exists
    if os.path.exists(dst):
        print(
            f"[clean_react_app->copy_directory()]: Destination directory {dst} already exists."
        )
        return

    # Try copying the directory
    try:
        shutil.copytree(src, dst)
        print(
            f"[clean_react_app->copy_directory()]: Directory copied from {src} to {dst}"
        )
    except Exception as e:
        print(
            f"[clean_react_app->copy_directory()]: Error occurred while copying directory: {e}"
        )


def replace_react_dir(original_dir, clean_dir):
    print("\n")
    # Check if the directory exists
    if os.path.exists(original_dir):
        try:
            # Delete the directory
            shutil.rmtree(original_dir)
            print(
                f"[clean_react_app->replace_react_dir()]: The original directory {original_dir} has been deleted."
            )
            copy_directory(clean_dir, original_dir)
        except OSError as e:
            print(
                f"[clean_react_app->replace_react_dir()]: Error: {e.filename} - {e.strerror}."
            )
    else:
        print(
            f"[clean_react_app->replace_react_dir()]: The original directory {original_dir} does not exist."
        )


def replace_file(src_file, dest_file):
    print("\n")
    try:
        # Copy the source file to the destination file's location
        shutil.copy2(src_file, dest_file)
        print(
            f"[clean_react_app->replace_file()]: File {dest_file} replaced successfully!"
        )
    except FileNotFoundError:
        print("[clean_react_app->replace_file()]: File not found.")
    except PermissionError:
        print(
            "[clean_react_app->replace_file()]: Permission denied. Make sure you have appropriate permissions."
        )


# = = = = = = = = = = START OF PROGRAM
print(" = = = = = = = START OF clean_react_app PROGRAM = = = = = = = \n")

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Create a new React app and clean/erase some default files."
)
parser.add_argument("app_name", help="The name of the React app to create and clean.")
parser.add_argument(
    "-y",
    action="store_true",
    help="Execute 'npm start' automatically after cleaning React app",
)

args = parser.parse_args()

try:
    # Create a new react app
    subprocess.check_call(["npx", "create-react-app", args.app_name])
except subprocess.CalledProcessError as e:
    print(f"[clean_react_app]: Error occurred while creating React app: {e}")
    exit(1)

# Path to the src directory
root_react_dir = args.app_name
src_dir = os.path.join(args.app_name, "src")
public_dir = os.path.join(args.app_name, "public")
readme_file = os.path.join(args.app_name, "README.md")

clean_src_dir = "boilerplate_files/src"
clean_public_dir = "boilerplate_files/public"
clean_readme_file = "boilerplate_files/README.md"

replace_react_dir(src_dir, clean_src_dir)
replace_react_dir(public_dir, clean_public_dir)
replace_file(clean_readme_file, readme_file)

# Check if the "-y" parameter is provided
if args.y:
    # Check if directory exists
    if not os.path.exists(root_react_dir):
        print(
            f"[clean_react_app->checking clean React directory]: Directory {root_react_dir} does not exist."
        )

    try:
        # Change to the directory
        os.chdir(root_react_dir)

        # Execute the command
        process = subprocess.Popen("npm start", shell=True, stdout=subprocess.PIPE)
        output, error = process.communicate()
        # Print command output
        if output:
            print("[clean_react_app->npm start]: Output: \n", output.decode())
        # Print error
        if error:
            print("[clean_react_app->npm start]: Error: \n", error.decode())
    except Exception as e:
        print(
            f"[clean_react_app->npm start]: Error occurred while executing command: {e}"
        )
    sys.argv.remove("-y")

print(" = = = = = = = END OF clean_react_app PROGRAM = = = = = = = \n")
