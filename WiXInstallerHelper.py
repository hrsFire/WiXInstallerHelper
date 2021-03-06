#!/usr/bin/env python

# this script creates a *.wxs file for a setup.exe

import os
import os.path
import uuid
from folder import Folder
from configuration_folder import ConfigurationFolder
from configuration_file import ConfigurationFile
from folder import Folder
from file import File

# Load the configuration file
from own_configuration import *

def main():
    if os.path.exists(root_folder):
        folders_with_files = walk_through_folders(root_folder, configuration_structure, "")

        if show_files_and_folders:
            print("##################################")
            print("## Available files and folders: ##")
            print("##################################")
            for show in folders_with_files.all_folders():
                print("-> " + str(show))
                for show1 in show.all_folders():
                    print("    |-> " + str(show1))
                    for show2 in show1.all_folders():
                        print("        |-> " + str(show2))

            print("\n")

            print("####################")
            print("## Configuration: ##")
            print("####################")
            for show in configuration_structure.all_folders():
                print("-> " + str(show))
                for show1 in show.all_folders():
                    print("    |-> " + str(show1))
                    for show2 in show1.all_folders():
                        print("        |-> " + str(show2))

        features = ""
        directories = ""
        component_groups = ""

        # create the objects to build the final file
        group = create_essential_fragments(indention, folders_with_files, "", root_folder)

        group[0] = create_package(indention) + "\n\n" + group[0]

        # add product
        group[0] = create_product(indention, group[0])
        group[0] = create_feature(indention, "", feature_title_variable, 1, group[0])

        # add fragment tag
        group[1] = create_fragment(indention, group[1])
        group[2] = create_fragment(indention, group[2])

        file_content = create_wix(indention, group[0] + "\n" + group[1] + "\n" + group[2])

        # create the final file
        f = open(os.path.join(destination_folder, 'file.txt'), 'w')
        f.write(file_content)
        f.close()

        print("\n")
        print("##################")
        print("##  Successful  ##")
        print("##################")


def walk_through_folders(parent_folder, configuration_folder_structure, root_folder_name):
    if type(parent_folder) is not str:
        raise Exception

    if type(root_folder_name) is not str:
        raise Exception

    if type(configuration_folder_structure) is not ConfigurationFolder:
        raise Exception

    current_folder = Folder(root_folder_name)

    for dir in os.listdir(parent_folder):
        path = os.path.join(parent_folder, dir)

        if os.path.isdir(path):
            folder = Folder(dir)
            temp_conf_folder = None

            for conf_folder in configuration_folder_structure.all_folders():
                if str(folder) == str(conf_folder):
                    if conf_folder.is_excluded():
                        break
                    else:
                        current_folder.add_folder(walk_through_folders(os.path.join(str(parent_folder), str(folder)), conf_folder, str(folder)))
                        break

        if os.path.isfile(path):
            file = File(dir)
            is_excluded = True

            for extension in configuration_folder_structure.all_extensions():
                if extension == file.extension():
                    is_excluded = False
                    break

            is_excluded_file = False
            for conf_file in configuration_folder_structure.all_files():
                if str(file) == str(conf_file):
                    if conf_file.is_excluded():
                        is_excluded_file = True
                        break

            if is_excluded is False and is_excluded_file is False:
                current_folder.add_file(file)

    return current_folder


def create_directory(indention, folder, dirs, dirs_and_name, id_name, name_variable, has_indention = True):
    if type(indention) is not str:
        raise Exception

    if type(folder) is not Folder:
        raise Exception

    if type(dirs_and_name) is not str:
        raise Exception

    if type(dirs) is not str:
        raise Exception

    has_empty_value = False

    if dirs_and_name == "":
        has_empty_value = True

    tag_attributes = "Id=\"" + (directory_prefix + char + dirs_and_name.upper() if has_empty_value == False else id_name) + ("\" Name=\"" + name_variable + str(folder) if has_empty_value == False or name_variable != "" else "") + "\""
    string = create_tag(indention, "Directory", tag_attributes, dirs)

    return string

def create_component(indention, directory, file, dirs_and_name, directory_path):
    if type(indention) is not str:
        raise Exception

    if type(directory) is not str:
        raise Exception

    if type(file) is not File:
        raise Exception

    if type(dirs_and_name) is not str:
        raise Exception

    dirs_and_file = (dirs_and_name + char if len(dirs_and_name) > 0 else "") + str(file)

    tag_attributes = "Id=\"" + component_prefix + char + dirs_and_file.replace(".", char).upper() + "\" Guid=\"" + str(uuid.uuid4()) + "\""
    content_tag_attributes = "Id=\"" + file_prefix + char + dirs_and_file.replace(".", char).upper() + "\" Source=\"" + ressource_variable + directory_path + os.path.sep + str(file) + "\" KeyPath=\"yes\" Checksum=\"yes\""
    content = create_tag(indention, "File", content_tag_attributes, "")
    string = create_tag(indention, "Component", tag_attributes, content)

    return string

def create_component_group(indention, dirs_and_name, components, id_name, has_indention = True):
    if type(dirs_and_name) is not str:
        raise Exception

    if type(components) is not str:
        raise Exception

    has_empty_value = False

    if dirs_and_name == "":
        has_empty_value = True

    string = ""

    if components != "":
        tag_attributes = "Id=\"" + component_group_prefix + ("" if dirs_and_name == "" else char + dirs_and_name) + "\" Directory=\"" + (directory_prefix + char + dirs_and_name if has_empty_value == False else id_name) + "\""
        string = create_tag(indention, "ComponentGroup", tag_attributes, components)

    return string

def create_feature(indention, feature, title, level, component_group_refs):
    if type(feature) is not str:
        raise Exception

    if type(level) is not int:
        raise Exception

    tag_attributes = "Id=\"feature" + char + feature + "\" Title=\"" + title + "\" Level=" + str(level) + "\""
    string = create_tag(indention, "Feature", tag_attributes, component_group_refs)

    return string

def create_component_group_ref(indention, dirs_and_name, has_indention = True):
    if type(dirs_and_name) is not str:
        raise Exception

    tag_attributes = "Id=\"" + component_group_prefix + ("" if dirs_and_name == "" else char + dirs_and_name) + "\""
    string = create_tag(indention, "ComponentGroupRef", tag_attributes, "")

    return string

def create_fragment(indention, content):
    string = create_tag(indention, "Fragment", "", content)

    return string

def create_product(indention, content):
    tag_attributes = "Id=\"*\" Name=\"" + product_title_variable + "\" Language=\"" + product_language_variable + "\" Version=\"" + product_version_variable + "\" Manufacturer=\"" + product_manufacturer_variable + "\" UpgradeCode=\"" + product_upgrade_code_variable + "\" Codepage=\"65001\""
    string = create_tag(indention, "Product", tag_attributes, content)

    return string

def create_package(indention):
    tag_attributes = "InstallerVersion=\"" + package_installer_version + "\" Compressed=\"" + package_is_compressed_variable + "\" InstallScope=\"" + package_install_scope_variable + "\" Manufacturer=\"" + package_manufacturer_variable + "\" Description=\"" + package_description_variable + "\""
    string = create_tag(indention, "Package", tag_attributes, "")

    return string

def create_major_upgrade(indention):
    tag_attributes = "InstallerVersion=\"" + package_installer_version + "\" Compressed=\"" + package_is_compressed_variable + "\" InstallScope=\"" + package_install_scope_variable + "\" Manufacturer=\"" + package_manufacturer_variable + "\" Description=\"" + package_description_variable + "\""
    string = create_tag(indention, "Package", tag_attributes, "")

    return string

def create_wix(indention, content):
    string = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + "\n"
    string += "<Wix xmlns=\"http://schemas.microsoft.com/wix/2006/wi\">" + "\n"
    content = add_indention(indention, content)
    string += content + "\n"
    string += "</Wix>"

    return string

def add_indention(indention, string):
    lines = string.split("\n")
    new_string = ""

    for i, line in enumerate(lines):
        if line == "":
            new_string += "\n"
            continue

        new_string += indention + line

        if i < len(lines) -1:
            new_string += "\n"

    return new_string

def create_tag(indention, tag_name, tag_attributes, content):
    string = "<" + tag_name + " " + tag_attributes

    if content == "":
        string += " />"
    else:
        content = add_indention(indention, content)
        string += ">" + "\n" + content + "\n"
        string += "</" + tag_name + ">"

    return string

def create_essential_fragments(indention, folders_with_files, root_folder, base_folder, recursion_count = 0):
    if type(folders_with_files) is not Folder:
        raise Exception

    if type(root_folder) is not str:
        raise Exception

    dirs_and_name = root_folder.replace(base_folder, "").replace(os.path.sep, char)
    directory_path = root_folder.replace(base_folder, "")

    group = ["", "", ""]; # ComponentGroupRef ; Directory ; ComponentGroup
    components = ""
    areFilesInDirectory = False

    for i, file in enumerate(folders_with_files.all_files()):
        components += create_component(indention, folder_string(folders_with_files, os.path.sep), file, dirs_and_name, directory_path)
        areFilesInDirectory = True

        if i < len(folders_with_files.all_files()) -1:
            components += "\n"

    if areFilesInDirectory:
        new_string = create_component_group_ref(indention, dirs_and_name, False)
        group[0] += new_string

    group[2] += create_component_group(indention, dirs_and_name, components, install_folder_id, False)
    dirs = ""

    for i, current_folder in enumerate(folders_with_files.all_folders()):
        if group[0] != "":
            group[0] += "\n"

        if dirs != "":
            dirs += "\n"

        if group[2] != "":
            group[2] += "\n"

        new_group = create_essential_fragments(indention, current_folder, os.path.join(root_folder, str(current_folder)), base_folder, recursion_count + 1)
        group[0] += new_group[0]

        dirs += new_group[1]

        group[2] += new_group[2]

    group[1] += create_directory(indention, folders_with_files, dirs, dirs_and_name, install_folder_id if recursion_count == 0 else "", install_folder_variable if recursion_count == 0 else "", False)

    return group

def folder_string(folder, char, return_string = ""):
    if type(folder) is not Folder:
        raise Exception

    return_string = str(folder)

    if len(folder.all_folders()) > 0:
        return_string = folder_string(folder.all_folders()[0], return_string + char + str(folder.all_folders()[0]))

    return return_string




if __name__ == "__main__" : main()
