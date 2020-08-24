from subprocess import check_output
process_name = "a.exe"
seq1 = 'ABCD'
seq2 = 'DCBA'
print(int(check_output(process_name + " " + seq1 + " " + seq2, shell=True).decode()))
