import re
import os
# import yaml
import subprocess
import pdb
import string
# from git import Git
# import astChecker
# import customast

# stream = open('config','r')
# config = yaml.load(stream)

def walkDirectory(rootdir,exclude='test'):
  # p = re.compile(".*"+exclude)
  for root, dirs, files in os.walk(rootdir):
    for name in files:
      # if (os.path.splitext(name)[1][1:] == 'py') and not p.match(root):
      if (os.path.splitext(name)[1][1:] == 'py'):
        yield os.path.join(root,name)

def subDirectory(rootdir):
  return os.listdir(rootdir)

def changegittag(directory,tag):
  # g = Git(directory)
  # g.checkout(tag)
  os.chdir(directory)
  p = subprocess.Popen('git checkout '+tag,shell=True,stdout=subprocess.PIPE)


def getClassLength(s,baseLine,fileName):
  actualLineNumber = 0
  indefblock = False
  res = [0]
  result = []
  defpattern = re.compile(r"^\s*def\s+")
  inheredoc = False
  currentLine = baseLine
  heredocbeginpattern = re.compile(r'^r?"""')
  heredocendpattern = re.compile(r'.*"""$')
  omitlinepattern = re.compile(r"^\s+$|^\s*#")
  for line in s.split("\n"):
    baseLine += 1
    # not deal the comment and blank
    if omitlinepattern.match(line) or line.strip() == "":
      continue
    #deal with heredoc
    if inheredoc:
      if heredocendpattern.match(line.strip()):
        inheredoc = False
      continue
    if heredocbeginpattern.match(line.strip()):
      if heredocendpattern.match(line.strip()):
        if line.strip() != '"""' and line.strip() != 'r"""':
          pass
      else:
        inheredoc = True
      continue
    if indefblock:
      current_indent = len(line) - len(line.lstrip())
      if current_indent > res[-1]:
        continue
      else:
        indefblock = False
    actualLineNumber += 1
    if defpattern.match(line.strip()):
      indefblock = True
      current_indent = len(line) - len(line.lstrip())
      res[-1] = current_indent
  # if (actualLineNumber-1) >= config['classsize']:
  result.append((5,fileName,currentLine+1,actualLineNumber-1))
  return result

def getFunctionMetric(s,baseLine,fileName):
  actualLineNumber = 0
  depth = 0
  res = []
  result = []
  defpattern = re.compile(r"^\s*def\s+")
  inheredoc = False
  heredocbeginpattern = re.compile(r'^r?"""')
  heredocendpattern = re.compile(r'.*"""$')
  omitlinepattern = re.compile(r"^\s+$|^\s*#")
  for line in s.split("\n"):
    baseLine += 1
    # not deal the comment and blank
    if omitlinepattern.match(line) or line.strip() == "":
      continue
    #deal with heredoc
    if inheredoc:
      if heredocendpattern.match(line.strip()):
        inheredoc = False
      continue
    if heredocbeginpattern.match(line.strip()):
      if heredocendpattern.match(line.strip()):
        if line.strip() != '"""' and line.strip() != 'r"""':
          pass
      else:
        inheredoc = True
      continue
    actualLineNumber += 1
    current_indent = len(line) - len(line.lstrip())
    while len(res) >= 1 and current_indent <= res[-1][-1]:
      element = res.pop()
      # if element[2] - element[1] >= config['funclength']:
      result.append((2,fileName,element[0],element[2]-element[1]))
      if len(res) == 0:
        # if depth >= config['funcdepth']:
        result.append((3,fileName,element[0],depth))
        depth = 0
    if defpattern.match(line.strip()):
      if len(res) >= 1:
        res[-1][2] += 1
      res.append([baseLine,actualLineNumber,actualLineNumber,current_indent])
      depth = max(depth,len(res))
      #if len(res) >= config['funcdepth']:
        #result.append((3,fileName,str(res[-1][0]),str(len(res))))
    if len(res) >= 1 and current_indent > res[-1][-1]:
      res[-1][2] += 1
  # if depth >= config['funcdepth']:
  result.append((3,fileName,res[0][0],depth))
  while len(res) > 0:
    element = res.pop()
    # if element[2] - element[1] >= config['funclength']:
    result.append((2,fileName,element[0],element[2] - element[1]))
  return result

def getMetric(s,baseLine,fileName):
  res = []
  t = s.split("\n")[0].strip().split(" ")[0]
  if t == "def":
    res = getFunctionMetric(s,baseLine,fileName)
  elif t == "class":
    res1 = getFunctionMetric(s,baseLine,fileName)
    res2 = getClassLength(s,baseLine,fileName)
    res = res1 + res2
  return res

def usedImports(fileName,imports):
    present = set()
    exclude = string.digits + string.letters + "_"
    inheredoc = False
    heredocendpattern = re.compile(r'.*"""$')
    if len(imports) == 0:
      return present
    for line in open(fileName):
        if line.strip() == "" or line.strip()[0] == '#':
            continue
        here_idx = line.strip().find('"""')
        if here_idx != -1:
            before_setence = line.strip()[:here_idx]
            after_sentence = line.strip()[here_idx+3:]
            if inheredoc:
                inheredoc = False
                if after_sentence != "":
                    line = after_sentence
                else:
                    continue
            else:
                if heredocendpattern.match(after_sentence):
                    inheredoc = False
                else:
                    inheredoc = True
                if before_setence != "":
                    line = before_setence
                else:
                    continue
        else:
            if inheredoc:
                continue
        if line.strip().split()[0] in ['import','from']:
            continue
        singlequote = re.compile('\"+.*\"+')
        doublequote = re.compile('\'+.*\'+')
        line_without_singlequote = singlequote.sub('',line)
        line_without_quote = doublequote.sub('',line_without_singlequote)
        for item in imports:
            idx = line_without_quote.find(item[0])
            #idx = line.find(item)
            if idx != -1:
                start = idx
                end = start + len(item[0]) - 1
                if start != 0:
                    before_letter = line_without_quote[start-1]
                    #before_letter = line[start-1]
                    if before_letter in exclude:
                        continue
                if end != len(line_without_quote) - 1:
                    after_letter = line_without_quote[end+1]
                    if after_letter in exclude:
                        continue
                present.add(item[0])
    return present

def execute(fileName):
  res = []
  currentContent = ""
  omitlinepattern = re.compile(r"^\s+$|^\s*#")
  baseLine = 0
  prevLines = 0

  with open(fileName) as f:
    for line in f:
      prevLines += 1
      if len(line) - len(line.lstrip()) == 0 and not omitlinepattern.match(line):
        if currentContent != "":
          res += getMetric(currentContent,baseLine,fileName)
          baseLine += prevLines - 1
          prevLines = 1
        currentContent = "" + line
        continue
      currentContent += line
  res += getMetric(currentContent,baseLine,fileName)
  return res


if __name__ == '__main__':
  pass
  # myast = astChecker.MyAst()
  # myast.fileName = "test.py"
  # astContent = customast.parse_file("test.py")
  # myast.visit(astContent)
  # print "imports:",myast.imports
  # usedImports = usedImports("test.py",myast.imports)
  # print "used imports:",usedImports
  # for defitem in myast.imports:
  #   for useitem in usedImports:
  #     if useitem == defitem[0]:
  #       break
  #   else:
  #     myast.result.append((8,defitem[1],defitem[2],defitem[0]))
  # print "Unused imports:"
  # print myast.result
