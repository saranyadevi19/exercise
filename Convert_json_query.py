#!/usr/bin/env python
##############################################################
##
## Generates the SQL queries from the JSON files
##
##############################################################
import os
import sys
import json
from pprint import pprint
import sqlite3
import glob
from subprocess import Popen, PIPE

def help():
   print "The script generates the SQL DML(insert and delete) queries from the JSON files. \nThe json files should be placed under the same directory where the script is placed. \nThe Execute and the Fallback file names should be passed by the user during the script execution. \nplease refer the files in the path :Database/ref/dml_patch"

def last_flagged(seq):
   seq = iter(seq)
   a = next(seq)
   for b in seq:
      yield a, False
      a = b
   yield a, True

def print_upper(str):
   output = "".join(["_"+ ch if ch.isupper() else ch for ch in str])
   if output[0] == "_":
      output = output[1:].upper()
      check_length(output)
   return output

def check_length(str):
   if len(str) > 30:
      print "ERROR: The length is greater than 30 characters for the string :" + str

def write_patch(str):
   patch.write(str)
   patch.write("\n")

def write_fallback(str):
   fallback.write(str)
   fallback.write("\n")

if __name__ == "__main__":
   if len(sys.argv) > 1:
      if sys.argv[1] == "-h":
         help()
         exit()

   print("Convert JSON")

   j=0
   meta_data_files = glob.glob("*.json")

   input_patch = raw_input('Enter the name for the execute file [File name format should be execute_<WO>.sql]:')
   print ('The name of the execute file: ', input_patch)
   input_fallback = raw_input('Print the name for the fallback file [File name format should be fallback_<WO>.sql]:')
   print ('The name of the fallback file: ', input_fallback)


   dummy_list1 = []
   #create one table for each meta-data file
   #order given by the array, with considering fks
   for meta_data_file in meta_data_files:

      with open(meta_data_file) as data_file:
         data = json.load(data_file)

         table = data["entityName"]["prefix"] +  data["entityName"]["name"]
         tableName = print_upper(table)

         pk_attribute_list = []
         invariant_list = []
         index_list = []
         for constraint in data["constraints"]:
            dummy_list = []
            fk_attribute_list = ()
            fk_reference_list = ()

            if constraint["name"] ==  "PrimaryKey":
               for field in constraint["fields"]:
                  pk_attribute_list.append(print_upper(field["name"]))

            if constraint["type"] ==  "Invariant":
               invariant_name = print_upper(constraint["name"])
               for field in constraint["fields"]:
                  invariant_list.append(print_upper(field["name"]))

            #Collect the Foriegn Key information from JSON
            if constraint["type"] == "SQLFK":
               fk_name = print_upper(constraint["name"])
               for field in constraint["fields"]:
                  fk_attribute_list += (print_upper(field["name"]), )

               for reference in constraint["reference"]["fields"]:
                  fk_reference_list += (print_upper(reference["name"]),)
               fk_table = constraint["reference"]["entityName"]["prefix"]+constraint["reference"]["entityName"]["name"]

               dummy_list.append(fk_name)
               dummy_list.append(fk_attribute_list)
               dummy_list.append(print_upper(fk_table))
               dummy_list.append(fk_reference_list)
               dummy_list.append(tableName)
               dummy_list1.append(dummy_list)

         #Collect the index information from JSON
         for index in data["indexes"]:
            index_name = index["name"]
            index_dummy_list = []
            index_attribute_list = ()

            for index_field in index["fields"]:
               ind = print_upper(index_field["name"])
               index_attribute_list += (ind, )

            index_dummy_list.append(index_name)
            index_dummy_list.append(index_attribute_list)

            index_list.append(index_dummy_list)

         if len(tableName) > 30 :
            print "ERROR : The Table Name : " + tableName + " has more than 30 characters."
            continue

         patch = open(input_patch, 'a')
         fallback = open(input_fallback, 'a')

         write_patch("------------------------EZT_TABLE-------------------------")
         statement = "INSERT INTO EZT_TABLE (TABLE_NAME, VERSION_NB, SHORTNAME, TABLE_INDEX, IS_GENERIC_TABLE,  DISPLAY_NAME) VALUES ('" + tableName + "' ,1 ,'RAIL"+str(j)+"' ,null ,'Y' ,null);"
         write_patch(statement)
         j = j + 1

         k=0
         for attribute,is_last in last_flagged(data["attributes"]):
            attr = print_upper(attribute["name"])

            if len(attr) > 30:
               print "ERROR : The Column Name : " + attr + " has more than 30 characters."
               break

            for pk,is_last_pk in last_flagged(pk_attribute_list):
               if pk == attr :
                  i = "1"
                  if attribute["type"] == "string":
                     stat = ' VARCHAR2(' + str(attribute["maxLength"]) + ')'
                  elif attribute["type"] == "int":
                     stat = " NUMBER"
                  elif attribute["type"] == "date-time":
                     stat = " DATE"
                  elif attribute["type"] == "date":
                     stat = " DATE"
                  elif attribute["type"] == "bool":
                     stat = " NUMBER"
                  else:
                     raise Exception("Unknown type " + attribute["type"])

                  break
               else:
                  i = "0"
                  if attribute["type"] == "string":
                     stat = ' VARCHAR2(' + str(attribute["maxLength"]) + ')'
                  elif attribute["type"] == "int":
                     stat = " NUMBER"
                  elif attribute["type"] == "date-time":
                     stat = " DATE"
                  elif attribute["type"] == "date":
                     stat = " DATE"
                  elif attribute["type"] == "bool":
                     stat = " NUMBER"
                  else:
                     raise Exception("Unknown type " + attribute["type"])

            for index,is_last_index_field in last_flagged(index_list):
               if index == attr :
                  ind = "Y"
                  break
               else:
                  ind = "N"

            if attribute["mandatory"]:
               isNull = "N"
            else:
               isNull = "Y"

            reg = attribute.get('regexp', 'null')

            statement = "INSERT INTO EZT_COLUMN_DEF (COLUMN_NAME, SHORTNAME, TABLE_NAME, IS_KEY, SQL_TYPE, CPP_TYPE, IS_INDEXED, CAN_BE_NULL, USERFORMAT, DEFAULT_VALUE, REGEXP) VALUES( '" + attr + "', '" +attr[:4]+str(k)+"', '" + tableName + "', '" + i + "', '" + stat + "', '" + attribute["type"] + "', '" + ind + "', '" + isNull + "',  null, null, '" + reg +"' );"

            write_patch(statement)

            if i == "1":
               statement = "INSERT INTO EZT_CONSTRAINT (CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, CONSTRAINT_TYPE_ID, REFERENCE_TABLE_NAME, REFERENCE_COLUMN_NAME)  VALUES ( 'PKEY"+str(k)+"', '" + tableName + "', '" + attr + "', 3, null, null);"
               write_patch(statement)

            k = k + 1

         # Make entry in the EZT_INDEX table
         if index_list:
            write_patch("-------------------EZT_TABLE_INDEX-------------------")
            for item in index_list:
               it = print_upper(item[0]) + "_IDX"
               check_length(it)
               l = 0
               for tuple,last_index in last_flagged(item[1]):
                  statement = "INSERT INTO EZT_TABLE_INDEX (TABLE_NAME,COLUMN_NAME, INDEX_NAME, POSITION_IN_INDEX, COLUMN_ASC) VALUES ( '"+ tableName + "', '" + tuple + "', '" + it + "', "+ str(l) +", 'Y');"
                  l=l+1
                  write_patch(statement)

         # Make entry in the EZT_CONSTRAINT table for Invariant
         if invariant_list:
            write_patch("-------------------EZT_CONSTRAINT for Invariant--------------------------")
            for invariant,is_last_in in last_flagged(invariant_list):
               statement = "INSERT INTO EZT_CONSTRAINT (CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, CONSTRAINT_TYPE_ID, REFERENCE_TABLE_NAME, REFERENCE_COLUMN_NAME)  VALUES ( '"+ invariant_name +"', '" + tableName + "', '" + invariant + "', 2, null, null );"
               write_patch(statement)

         write_patch("-------------------EZT_PUBLICATION--------------------------")
         statement = "INSERT INTO EZT_PUBLICATION (TABLE_NAME, PACKAGE_NAME) VALUES ('" + tableName + "', 'rail_pack');"
         write_patch(statement)

         write_fallback("-----------------------------------------FALLBACK-------------------------------------")

         statement = "DELETE from EZT_TABLE_INDEX where TABLE_NAME = '"+ tableName +"';";
         write_fallback(statement)

         statement = "DELETE from EZT_CONSTRAINT where TABLE_NAME = '"+ tableName +"';";
         write_fallback(statement)

         statement = "DELETE from EZT_COLUMN_DEF where TABLE_NAME = '"+ tableName +"';";
         write_fallback(statement)

         statement = "DELETE from EZT_PUBLICATION where TABLE_NAME = '"+ tableName +"';";
         write_fallback(statement)

         statement = "DELETE from EZT_TABLE where TABLE_NAME = '"+ tableName +"';";
         write_fallback(statement)

   # Make entry in the EZT_CONSTRAINT table for foreign key
   if dummy_list1:
      write_patch("-------------------EZT_CONSTRAINT for Foreign key-------------------------")
      for fk_avail,last_fk_avail in last_flagged(dummy_list1):
         for fk_col, fk_ref_col in zip(fk_avail[1],fk_avail[3]):
            statement = "INSERT INTO EZT_CONSTRAINT (CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, CONSTRAINT_TYPE_ID, REFERENCE_TABLE_NAME, REFERENCE_COLUMN_NAME)  VALUES ( '" + fk_avail[0].upper() + "', '" + fk_avail[4] + "', '" + fk_col + "',1 ,'" + fk_avail[2] + "', '" + fk_ref_col + "' );"
            write_patch(statement)
   print("Executed successfully")
