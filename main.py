#import imp
from multiprocessing.sharedctypes import Value
from pyexpat import model
from re import M
#from readline import append_history_file
import numpy as np
#import metriculous
import sys
import csv
#from configparser import ConfigParser
import configparser
import csv
import pandas as pd
from itertools import groupby
from sklearn import preprocessing
import metriculous

le = preprocessing.LabelEncoder()

n_arguments = len(sys.argv)
print("Total number of command line arguments passed: ", n_arguments)
num_models = n_arguments - 2
print("Total number of models to compare: ", num_models)

#config_file = open(config_file, "r")
#content = config_file.read()
#print("Content of the config file are:\n")
#print(content)

#The second argument is the config file
#We open,read the config file and convert each key-value pairs in the dictionary 
config_file = sys.argv[1]
dictionary = {}
#cfg = ConfigParser()
#cfg.read(config_file)


cfg = configparser.RawConfigParser()
cfg.optionxform = str
#cfg.optionxform = lambda option: option.upper()
cfg.read(config_file)
#cfg.defaults()

#config_file.flush()
for sections in cfg.sections():
    print(sections)
    dictionary[sections] = {}
    #dictionary = dict()
    for option in cfg.options(sections):
        dictionary[sections][option] = cfg.get(sections, option)
        dictionary[option] = cfg.get(sections, option)

print(dictionary)

models = dict()
ground_truth_dic = dict()
class_names_dic = dict()
dilution_dic = dict()

#The model files strart from the third argument of the command line
for i in range(2,n_arguments,1):

    data_file = sys.argv[i]
    print(data_file)
    model_name = "model_" + str(i-1)
    print(model_name)
    predictions = []
    ground_truth_array = []
    dilution_array = []
    
    results = pd.read_csv(data_file)
    print("Number of samples (patients) in the model file: ")
    num_patients = len(results)
    print(num_patients)
    
    

    with open(data_file, 'r') as my_file:
        reader = csv.DictReader(my_file)
        fieldnames = reader.fieldnames
        print(fieldnames)
        total = len(fieldnames)

        class_names = []
        for i in range(2,total):
                class_names.append(fieldnames[i])
        
        print("Class names: ")
        print(class_names)

        #class_names_num = [idx for idx, (k, v) in enumerate(groupby(class_names), 0) for i in v]
        #print("Class names to numbers: ")
        #print(class_names_num)
        
        a = le.fit(class_names) #do label encoding of the classes
        print("Labeled class names: ")
        print(a)

        class_names_dic[model_name] = class_names


    
        csv_reader = csv.reader(my_file)#, delimiter = '\t')
        

        for row in csv_reader:
            
            print(row)
            print("Number of elements in the row: ", len(row))
            
        
            dilution = row[0]
            print(dilution)
            dilution_array.append(dilution) #Array with dillutions for each sample of the model
           
            ground_truth = row[1]
            print(ground_truth)
            ground_truth_array.append(ground_truth) #Array with ground truth for each sample of the model

            
            model_predictions = []
            for k in range(2,total):
                model_predictions.append(row[k])
                


            print("Model predictions: ")
            print(model_predictions)
            
            model_predictions = [eval(i) for i in model_predictions]
            
            print("Modified list of predictions is: ", model_predictions)
            
            
            predictions.append(model_predictions)
            #models[model_name] = model_predictions
            #predictions = np.append(model_predictions)
            print("Predictions: ")
            print(predictions)
            models[model_name] = predictions
            print(models)
    
    #ground_truth_array = [eval(i) for i in ground_truth_array]
    #ground_truth_array = [idx for idx, (k, v) in enumerate(groupby(ground_truth_array), 0) for i in v]
    #print(ground_truth_array)
    ground_truth_array = list(le.transform(ground_truth_array))
    print(ground_truth_array)
    ground_truth_dic[model_name] = ground_truth_array


    print("Dilution array: ")
    print(dilution_array)
    for k in range(len(dilution_array)):
        if dilution_array[k] == '':
            dilution_array[k] = '1'

    print("Dilution array: ")
    print(dilution_array)
    dilution_array = [eval(i) for i in dilution_array]
    dilution_dic[model_name] = dilution_array
    print("Ground Truth Dictionary: ")
    print(ground_truth_dic)  
    print("Class Names Dictionary: ")
    print(class_names_dic)  
    print("Dilution Dictionary: ")
    print(dilution_dic)
     
quantity_list = []
figure_list = []
threshold_dic = dict()

for sections in dictionary.keys():
    if sections == "quantity":
        for metric, value in dictionary['quantity'].items():
            if value == 'no':
                quantity_list.append(metric)
    elif sections == "figures":
         for metric, value in dictionary['figures'].items():
            if value == 'no':
                figure_list.append(metric)
    elif sections == "threshold":
         for class_name, value in dictionary['threshold'].items():
            threshold_dic[class_name] = value



print("Quantities that have to be excluded: ")
print(quantity_list)

print("Figures that have to be excluded: ")
print(figure_list)

print("Dictionary of thresholds for each class: ")
print(threshold_dic)

filter_quantity_list = lambda x: x not in quantity_list
filter_figure_list = lambda x: x not in figure_list


ground_truth_argument = ground_truth_dic.get(list(ground_truth_dic.keys())[0])
print(ground_truth_argument)

dilution_argument = dilution_dic.get(list(dilution_dic.keys())[0])
print(dilution_argument)

print(models)

model_predictions_array = []

for i in range(num_models):
    model_predictions_array.append(list(models.values())[i])

print(len(model_predictions_array))

if (len(threshold_dic.keys()) == len(class_names)):
    if(len(quantity_list)!=0 and len(figure_list)!=0):
        metriculous.compare_classifiers(
            ground_truth=ground_truth_argument,
            model_predictions=model_predictions_array,
            model_names= list(class_names_dic.keys()),
            class_names=class_names,
            dilution=dilution_argument,
            filter_quantities= filter_quantity_list,
            filter_figures= filter_figure_list,
            one_vs_all_figures=True,
            ).save_html("comparison1.html").display()
    elif (len(quantity_list)==0 and len(figure_list)!=0):
        metriculous.compare_classifiers(
            ground_truth=ground_truth_argument,
            model_predictions=model_predictions_array,
            model_names= list(class_names_dic.keys()),
            class_names=class_names,
            dilution=dilution_argument,
            filter_figures= filter_figure_list,
            one_vs_all_figures=True,
            ).save_html("comparison1.html").display()
    elif (len(quantity_list)!=0 and len(figure_list)==0):
        metriculous.compare_classifiers(
            ground_truth=ground_truth_argument,
            model_predictions=model_predictions_array,
            model_names= list(class_names_dic.keys()),
            class_names=class_names,
            dilution=dilution_argument,
            filter_quantities= filter_quantity_list,
            one_vs_all_figures=True,
            ).save_html("comparison1.html").display()
    else:
        metriculous.compare_classifiers(
            ground_truth=ground_truth_argument,
            model_predictions=model_predictions_array,
            model_names= list(class_names_dic.keys()),
            class_names=class_names,
            dilution= dilution_argument,
            one_vs_all_figures=True,
            ).save_html("comparison1.html").display()
        
        
       
else:
    print("Number of set thresholds for the classes is not compatible with the number of classes in the model files.")



