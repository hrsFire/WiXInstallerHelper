from configuration_folder import ConfigurationFolder
from configuration_file import ConfigurationFile

# some common settings
indention = "   "
char = "_"
directory_prefix = "DIR"
file_prefix = "FILE"
component_prefix = "CMP"
component_group_prefix = "CMPGROUP"
show_files_and_folders = True


### start of you own common configuration
program_files_folder_id = "ProgramFilesFolder"
subdirectory_id = "SubDirectory"
install_folder_id = "INSTALLFOLDER"

root_folder = "../RD_Messdatenbank_AIS/GUI/bin/Release/"
ressource_variable = "$(var.AISProjectDirectory)"
destination_folder = "./"
subdirectory_variable = "$(var.Manufacturer)"
install_folder_variable = "$(var.InstallFolder)"
feature_title_variable = "!(loc.ProductName)"
product_title_variable = feature_title_variable
product_version_variable = "$(var.Version)"
product_manufacturer_variable = "$(var.Manufacturer)"
product_upgrade_code_variable = "e8d1220f-e31a-41c8-9289-b83b77e4b8e2"
product_language_variable = "1033"
package_installer_version = "200"
package_is_compressed_variable = "yes"
package_install_scope_variable = "perMachine"
package_manufacturer_variable = product_manufacturer_variable
package_description_variable = "!(loc.Description)"

### end of you own common configuration


### start of your own file and folder configuration
## info: we do not map folders or files

configuration_structure = ConfigurationFolder(install_folder_id)
configuration_structure.add_extension("exe")
configuration_structure.add_extension("config")
configuration_structure.add_extension("dll")
configuration_structure.add_extension("xml")

temp_folder = ConfigurationFolder("de", False, True)
temp_folder.add_extension("dll")
configuration_structure.add_folder(temp_folder)

temp_folder = ConfigurationFolder("en", False, True)
temp_folder.add_extension("dll")
configuration_structure.add_folder(temp_folder)

temp_folder = ConfigurationFolder("es", False, True)
temp_folder.add_extension("dll")
configuration_structure.add_folder(temp_folder)

temp_folder = ConfigurationFolder("fr", False, True)
temp_folder.add_extension("dll")
configuration_structure.add_folder(temp_folder)

temp_folder = ConfigurationFolder("it", False, True)
temp_folder.add_extension("dll")
configuration_structure.add_folder(temp_folder)

temp_folder = ConfigurationFolder("nl", False, True)
temp_folder.add_extension("dll")
configuration_structure.add_folder(temp_folder)

temp_folder = ConfigurationFolder("tr", False, True)
temp_folder.add_extension("dll")
configuration_structure.add_folder(temp_folder)

temp_folder = ConfigurationFolder("Controllers", False, True)
temp_folder2 = ConfigurationFolder("AIS_HQLib", False, True)
temp_folder2.add_extension("pyd")
temp_folder2.add_extension("dll")
temp_folder2.add_extension("zip")
temp_folder.add_folder(temp_folder2)
configuration_structure.add_folder(temp_folder)

temp_folder = ConfigurationFolder("Equipments", False, True)
temp_folder2 = ConfigurationFolder("Tektronix", False, True)
temp_folder3 = ConfigurationFolder("TDS_3045B", False, True)
temp_folder3.add_extension("dll")
temp_folder2.add_folder(temp_folder3)
temp_folder.add_folder(temp_folder2)
configuration_structure.add_folder(temp_folder)

# excluded files and folders
configuration_structure.add_file(ConfigurationFile("AIS.vshost.exe", True))
configuration_structure.add_file(ConfigurationFile("AIS.vshost.exe.config", True))
configuration_structure.add_folder(ConfigurationFolder("app.publish", True))

### end of your own file and folder configuration