from webbrowser import open_new_tab
import os
from htmlModule import *


# SETTINGS
wd = 'E:\\DATA\\20211022_ILSLD_PA_K501_LED非点灯\\DriverIC_U7&U9_出力電圧比較'
cwd = os.getcwd()
filelist = os.listdir(wd)
filelist = list(filter(lambda x: x.endswith('.jpg'), filelist))
out_file = wd + '/' + 'Image_comparator.html'
tag_name = 'ILSLD K501 025 U7&U9'

# Read html base file
# temp_wrapper = 'temp_wrapper.html'
# htmlFile = open(temp_wrapper, 'r', encoding='UTF-8')
# base = htmlFile.read()
base = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>%s</title>
</head>
<body>
<table border="1">
</table>
</body>
</html>
"""

# Repeat pattern
wrapper = """
<tr>
  <td>%s<img src=%s></td>
  <td>%s<img src=%s></td>
</tr>
"""

body = ''
# 2 COLUMNS VER.
# In the case of 1 column missing
if len(filelist)%2 == 1:
    filelist.append('None')
# Add wrapper-str to <body>
for i in range(len(filelist)//2):
    body = body + wrapper
# Insert content to <table>
index = base.find('</table>')
base = base[:index] + body + base[index:]

# Divide filelist into 2 filelists
# Upper/Lower
filelist0 = filelist[:len(filelist)//2]
filelist1 = filelist[len(filelist)//2:]
# Odd/Even
# filelist0, filelist1 = get_oddeven(filelist)

# Make a tuple for wrapper
wrap_info = [tag_name]
for f0,f1 in zip(filelist0, filelist1):
    wrap_info.append(f0)  # Title
    wrap_info.append(f0)  # Image
    wrap_info.append(f1)  # Title
    wrap_info.append(f1)  # Image
# List to tuple (for wrapper)
wrap_info = tuple(wrap_info)

# WRAPPER
main = base % wrap_info
# Explanation
# main = base % (filelist0[0], filelist1[0],
#                filelist0[1], filelist1[1],
#                   :
#                   )

# OUTPUT
f = open(out_file, 'w')
f.write(main)
f.close()

# SHOW
open_new_tab(out_file)

print('filelist:\n', filelist)

