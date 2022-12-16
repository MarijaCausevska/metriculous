import configparser
#import ConfigParser

# CREATE OBJECT
#config_file = configparser.ConfigParser()

config_file = configparser.RawConfigParser()
config_file.optionxform = str
# ADD SECTION
config_file.add_section("quantity")
# ADD SETTINGS TO SECTION



config_file.set("quantity", "Accuracy", "yes")
config_file.set("quantity", "ROC AUC Macro Average", "no")
config_file.set("quantity", "ROC AUC Micro Average", "no")
config_file.set("quantity", "F1-Score Macro Average", "no")
config_file.set("quantity", "F1-Score Micro Average", "yes")
config_file.set("quantity", "Log Loss", "yes")
config_file.set("quantity", "Mean KLD(P=target||Q=prediction)", "yes")
config_file.set("quantity", "Brier Score Loss", "yes")
config_file.set("quantity", "Brier Score Loss (Soft Targets)", "yes")
config_file.set("quantity", "Max Entropy", "yes")
config_file.set("quantity", "Min Entropy", "yes")
config_file.set("quantity", "Max Probability", "no")
config_file.set("quantity", "Min Probability", "yes")

config_file.add_section("figures")
config_file.set("figures", "Class Distribution", "yes")
config_file.set("figures", "Confusion Scatter Plot", "yes")
config_file.set("figures", "Automation Rate Analysis", "yes")
config_file.set("figures", "Confusion Matrix", "yes")
config_file.set("figures", "ROC", "no")
config_file.set("figures", "PR", "yes")
config_file.set("figures", "Mosaic of the samples with a given dilution", "no")

config_file.add_section("threshold")
config_file.set("threshold", "model_1", "0.7")
config_file.set("threshold", "model_2", "0.6")





# SAVE CONFIG FILE
with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print("Config file 'configurations.ini' created")

# PRINT FILE CONTENT
read_file = open("configurations.ini", "r")
content = read_file.read()
print("Content of the config file are:\n")
print(content)
read_file.flush()
read_file.close()