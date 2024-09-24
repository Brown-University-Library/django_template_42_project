"""
Purpose:
- Renames all project and app references from foo_project and foo_app to the desired project and app names.

Usage:
$ python ./update_project_and_app_references.py --target_dir "/path/to/foo_project/" --new_project_name "bar_project" --new_app_name "bar_app" 

Note: 
- This script will delete the git-cloned `.git` directory in the target directory, so you can start a new git repository.
"""

import argparse, os, shutil, stat, traceback
from pathlib import Path, PosixPath, WindowsPath
from typing import Callable, Tuple


## constants --------------------------------------------------------
REPO_PROJECT_NAME = 'django_template_42_project'    # raw git-clone name
OLD_PROJECT_NAME = 'foo_project'                    # all the internal code project-references
OLD_APP_NAME = 'foo_app'


## helper functions -------------------------------------------------


def rename_top_level_directory( target_directory: Path, new_project_name: str ) -> Path:
    """ Renames the top-level project directory if needed.
        Called by run_updater(). """
    if REPO_PROJECT_NAME in target_directory.name:
        new_directory: Path = target_directory.with_name(
            target_directory.name.replace( REPO_PROJECT_NAME, new_project_name )
        )
        target_directory.rename( new_directory )
        return_dir: Path = new_directory
    else:
        return_dir: Path = target_directory
    return return_dir


def rename_files_and_directories( target_directory: Path, new_project_name: str, new_app_name: str ) -> None:
    """ Renames any files and directories in the target directory. 
        Called by run_updater. """
    for item in target_directory.rglob('*'):
        assert isinstance(item, (PosixPath, WindowsPath)), f"Unexpected path type: {type(item)}"
        if item.is_dir():
            if OLD_PROJECT_NAME in item.name:
                new_dir_name: str = item.name.replace( OLD_PROJECT_NAME, new_project_name )
                item.rename( item.with_name(new_dir_name) )
            elif OLD_APP_NAME in item.name:
                new_dir_name: str = item.name.replace( OLD_APP_NAME, new_app_name )
                item.rename( item.with_name(new_dir_name) )
        elif item.is_file():
            if OLD_PROJECT_NAME in item.name:
                new_file_name: str = item.name.replace(OLD_PROJECT_NAME, new_project_name)
                item.rename( item.with_name(new_file_name) )
            elif OLD_APP_NAME in item.name:
                new_file_name: str = item.name.replace(OLD_APP_NAME, new_app_name)
                item.rename( item.with_name(new_file_name) )


def update_file_contents( target_directory: Path, new_project_name: str, new_app_name: str ) -> None:
    for item in target_directory.rglob( '*' ):
        assert isinstance(item, (PosixPath, WindowsPath)), f"Unexpected path type: {type(item)}"
        if item.is_file():
            if item.name == 'update_project_and_app_references.py':
                continue
            replace_in_file( item, OLD_PROJECT_NAME, new_project_name )
            replace_in_file( item, OLD_APP_NAME, new_app_name )
    return


def replace_in_file( file_path: Path, old_text: str, new_text: str ) -> None:
    """ Replaces old_text with new_text in the file at file_path. 
        Called by update_file_contents. """
    try:
        content = file_path.read_text( encoding='utf-8' )
        content = content.replace( old_text, new_text )
        file_path.write_text( content, encoding='utf-8' )
    except UnicodeDecodeError:
        pass  # skip files that can't be read as UTF-8
    return


def handle_remove_readonly( func: Callable, path: str, exc_info: Tuple ) -> None:
    """ Handles removing read-only files. 
        Called by delete_git_directory().
        Parameters:
            func: The function that raised the exception (e.g., `os.remove` or `os.rmdir`).
            path: The path to the file or directory that couldn't be removed.
            exc_info: sys.exc_info() info of exception type, value, and traceback.
        What's going on here...
        - This function handles a situation that, in testing, seems to appear on Windows.
        - My understanding is that git may set some config or metadata files within the `.git` directory 
          to be marked as read-only. These read-only files are handled differently in Windows than in a unix-like system,
          and may prevent the `.git` directory from being deleted until these read-only files are handled.
        - Only the `path` parameter is used, but shutil.rmtree() sends all three params if there's an error.
    """
    try:    
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:  
        ## to help clarify the original vs subsequent exceptions
        original_exception = ''.join( traceback.format_exception( *exc_info) )
        retry_exception = ''.join( traceback.format_exception_only(type(e), e) )
        print (f'Failed to delete ``{path}`` after changing permissions.' )
        print( f'Original exception, ``{original_exception}``' )
        print( f'Exception during retry, ``{retry_exception}``' )
        raise


def delete_git_directory(target_directory: Path) -> None:
    """ Deletes the .git directory in the target directory if it exists. 
        Called by run_updater. """
    git_dir: Path = target_directory / '.git'
    if git_dir.exists():
        if git_dir.is_dir():
            shutil.rmtree( git_dir, onerror=handle_remove_readonly )
            print( f'Deleted .git directory in ``{target_directory}``.' )
    else:
        print( f'No .git directory found at ``{git_dir}``.' )
    return


## manager functions ------------------------------------------------


def parse_args() -> None:
    """ Parses args and passes them to the main manager function.
        Called by dundermain. """
    ## configure argument parser
    parser = argparse.ArgumentParser(description='Update project and app references in a directory.')
    parser.add_argument('--target_dir', type=str, required=True, help='The directory to update.')
    parser.add_argument('--new_project_name', type=str, required=True, help='The new project name.')
    parser.add_argument('--new_app_name', type=str, required=True, help='The new app name.')
    args = parser.parse_args()
    ## get the values
    target_directory: Path = Path(args.target_dir)
    new_project_name: str = args.new_project_name
    new_app_name: str = args.new_app_name
    ## confirm target_directory exists
    if not target_directory.exists():
        raise FileNotFoundError( f'Target directory ``{target_directory}`` does not exist.' )
    ## run updater
    run_updater( target_directory, new_project_name, new_app_name )
    return


def run_updater( target_directory: Path, new_project_name: str, new_app_name: str ) -> None:
    """ Performs the update operations on the target directory. 
        Called by parse_args. """
    ## rename top-level directory if needed
    target_directory = rename_top_level_directory(
        target_directory, new_project_name
    )
    ## first pass: rename files and directories
    rename_files_and_directories( target_directory, new_project_name, new_app_name )
    ## second pass: update file contents
    update_file_contents( target_directory, new_project_name, new_app_name )
    ## delete .git directory
    delete_git_directory( target_directory )
    print( f'Updated project and app references in ``{target_directory}`` to ``{new_project_name}`` and ``{new_app_name}``.' )
    return


## dundermain -------------------------------------------------------
if __name__ == '__main__':
    parse_args()
