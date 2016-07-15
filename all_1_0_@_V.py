#! /usr/bin/python
import sys

OUTPUT_FILE = str(sys.argv[1])
all_records = [line.strip() for line in open('xx.txt', 'r')]

modified_records = {}

f2 = open(OUTPUT_FILE, "a")

for record in all_records:
    split_record = record.split(',')
    payment_id = split_record[23]
    sender_acc_no = split_record[1]
    receiver_acc_no = split_record[2]
    receiver_txn_id = split_record[0]
    sender_txn_id = split_record[0]
    amount = abs(int(split_record[4]))
    status = split_record[7]
    key = payment_id
    if len(str(split_record[0])) < 13 and split_record[3] == '@' and status == 'V':
      if key in modified_records:
        if (sender_acc_no in modified_records[key] or receiver_acc_no in modified_records[key]) and  str(amount) in modified_records[key] :
            new_record = modified_records[key] + "|" + receiver_txn_id
        else:
            new_record = modified_records[key] + "\n" + payment_id + "," + sender_acc_no + "," + receiver_acc_no + "," + str(amount) + "," + sender_txn_id
      else:
        new_record = payment_id + "," + sender_acc_no + "," + receiver_acc_no + "," + str(amount) + "," + sender_txn_id
      modified_records[key] = new_record

for k in modified_records:
#    print modified_records[k]
    f2.write(modified_records[k])
    f2.write("\n")

f2.close()
