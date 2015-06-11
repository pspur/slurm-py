import os
import re

mappedreads = []
for file in os.listdir("/user/paulspur/fstats"):
  if os.path.isfile(file) and file.endswith(".fstat"):
    f = open(file)
    lines = f.readlines()    
    m = re.search(r"(\d{1,2}\.\d{1,2})",lines[8])
    print(lines[8])
    f.close()
    print(m.group())         
# mappedreads.append(file[0:23]+','+ re.group())

for member in mappedreads:
  print(member)
