import os
import csv
import customast
import ast
from parameter import subject_dir

project_info_file = csv.writer(open('project_info.csv', 'w+b'))
project_info_file.writerow(['project', 'files', 'LOC'])
total_projects = 0
total_lines = 0
total_files = 0


def walkDirectory(rootdir):
  for root, dirs, files in os.walk(rootdir):
    for name in files:
      if (os.path.splitext(name)[1][1:] == 'py'):
        yield os.path.join(root, name)


def count_lines(node):
    childnodes = list(ast.walk(node))
    lines = [0]
    for n in childnodes:
        if hasattr(n, 'lineno'):
            lines.append(n.lineno)
    return max(lines)


projects = os.listdir(subject_dir)

for projectName in projects:
    total_projects += 1
    project_dir = subject_dir + projectName
    lines = 0
    files = 0
    for currentFileName in walkDirectory(project_dir):
        try:
            astContent = customast.parse_file(currentFileName)
        except:
            print project_dir, currentFileName
            continue
        lines = lines + count_lines(astContent)
        files = files + 1
    project_info_file.writerow([projectName, files, lines])
    total_lines = total_lines + lines
    total_files = total_files + files

project_info_file.writerow([total_projects, total_files, total_lines])