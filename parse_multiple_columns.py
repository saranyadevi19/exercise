#! /usr/bin/python
import sys

OUTPUT_FILE = str(sys.argv[1])
all_records = [line.strip() for line in open('dup_pay.csv', 'r')]

modified_records = {}

f2 = open(OUTPUT_FILE, "a")

for record in all_records:
    split_record = record.split(',')
    payment_id = split_record[1]
    sender_acc_no = split_record[4]
    receiver_acc_no = split_record[6]
    receiver_txn_id = split_record[0]
    sender_txn_id = split_record[0]
    key = payment_id
    if key in modified_records:
        if sender_acc_no in modified_records[key] or receiver_acc_no in modified_records[key]:
            new_record = modified_records[key] + "|" + receiver_txn_id
        else:
            new_record = modified_records[key] + "\n" + payment_id + "," + sender_acc_no + "," + receiver_acc_no + "," + sender_txn_id
    else:
        new_record = payment_id + "," + sender_acc_no + "," + receiver_acc_no + "," + sender_txn_id
    modified_records[key] = new_record
for k in modified_records:
    print modified_records[k]
    f2.write(modified_records[k])
    f2.write("\n")

f2.close()



----------------------INPUT FORMAT------------------------------------
Base ID,Payment ID,Type,Subtype,Account Number,Account Email ID,Counterparty,Flags,Flags2,Flags3,Flags4,Flags5,Amount,Currency^M
18668608367988061,18668608367965000,U,I,1984083041954134341,2590375475,1838556843316855404,38404176,2144,557088,256,99079191802150963,1900,USD^M
18668608367988060,18668608367965000,U,I,1838556843316855404,2590375475,1984083041954134341,37879888,2144,32800,256,99079191802150915,-1900,USD^M
18668608367988057,18668608367965000,H,,1838556843316855404,,,33554432,2048,32,0,18014398509481984,1900,USD^M
131939057274,18668608367965000,@,G,1556286613275624261,636417272,1699747819407366073,4456452,0,8945664,0,81064793292668930,1094,USD^M
131939057273,18668608367965000,@,G,1699747819407366073,636417272,1556286613275624261,4194308,256,8421376,0,81064793292668930,-1094,USD^M
18668608368536694,18668608368529962,U,I,1549236293606715118,938046319,1262198895459737768,4980816,268435552,622592,256,99079191802150963,2874,USD^M
18668608368536693,18668608368529962,U,I,1262198895459737768,938046319,1549236293606715118,4194384,268435808,98304,256,99079191802150915,-2874,USD^M
18668608368536690,18668608368529962,X,C,1262198895459737768,,,0,0,0,0,18014398509481984,2874,USD^M
18668608368536689,18668608368529962,X,C,1262198895459737768,,,0,0,0,0,18014398509481984,-4028,AUD^M
18668608368536685,18668608368529962,R,,1262198895459737768,,,0,0,0,0,18014398509481984,4028,AUD^M
131939103832,18668608368529962,@,G,1600917856147284855,598179286,1500200365198182058,4456452,256,8945664,0,81064793292668930,2036,USD^M
131939103831,18668608368529962,Q,A,1500200365198182058,,,1,0,0,0,0,-2036,USD^M
131939103830,18668608368529962,@,G,1500200365198182058,598179286,1600917856147284855,4456452,256,8421888,0,81064793292668930,-2036,USD^M


--------------------------------------------------------- output------------------------------
fThe payment_id is populated for 2 buyer and 2 seller.
This helps to avoid that
