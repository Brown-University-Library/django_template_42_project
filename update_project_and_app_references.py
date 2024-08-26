"""
Purpose:
- Renames all project and app references from foo_project and foo_app to the desired project and app names.

Usage:
$ python ./update_project_and_app_references.py --target_dir "/path/to/foo_project" --new_project_name bar_project --new_app_name bar_app 
"""

import argparse
from pathlib import Path


## helper functions -------------------------------------------------

def rename_files_and_directories(
        target_directory: Path, 
        old_project_name: str, 
        new_project_name: str, 
        old_app_name: str, 
        new_app_name: str ) -> None:
    """ Renames any files and directories in the target directory. 
        Called by run_updater. """
    for item in target_directory.rglob( '*' ):
        assert type(item) == Path
        if item.is_dir():
            if old_project_name in item.name:
                new_dir_name: str = item.name.replace( old_project_name, new_project_name )
                item.rename( item.with_name(new_dir_name) )
            elif old_app_name in item.name:
                new_dir_name: str = item.name.replace( old_app_name, new_app_name )
                item.rename( item.with_name(new_dir_name) )
        elif item.is_file():
            if old_project_name in item.name:
                new_file_name: str = item.name.replace(old_project_name, new_project_name)
                item.rename( item.with_name(new_file_name) )
            elif old_app_name in item.name:
                new_file_name: str = item.name.replace(old_app_name, new_app_name)
                item.rename( item.with_name(new_file_name) )


def update_file_contents( 
        target_directory: Path, 
        old_project_name: str, 
        new_project_name: str, 
        old_app_name: str, 
        new_app_name: str ) -> None:
    for item in target_directory.rglob( '*' ):
        assert type(item) == Path
        if item.is_file():
            replace_in_file( item, old_project_name, new_project_name )
            replace_in_file( item, old_app_name, new_app_name )
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
    old_project_name = 'foo_project'
    old_app_name = 'foo_app'
    ## run updater
    run_updater( target_directory, old_project_name, new_project_name, old_app_name, new_app_name )
    return

def run_updater( 
        target_directory: Path, 
        old_project_name: str, 
        new_project_name: str, 
        old_app_name, new_app_name: str ) -> None:
    """ Performs the update operations on the target directory. 
        Called by parse_args. """
    ## first pass: rename files and directories
    rename_files_and_directories(
        target_directory, 
        old_project_name, 
        new_project_name, 
        old_app_name, 
        new_app_name )
    ## second pass: update file contents
    update_file_contents( 
        target_directory, 
        old_project_name, 
        new_project_name, 
        old_app_name, 
        new_app_name )
    print( f'Updated project and app references in {target_directory} to {new_project_name} and {new_app_name}.' )
    return


## dundermain
if __name__ == '__main__':
    parse_args()