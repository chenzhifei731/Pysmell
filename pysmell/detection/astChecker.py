import ast,_ast
import re
import customast
import astunparse
# import yaml

# stream = open("config",'r')
# config = yaml.load(stream)

class MyAst(ast.NodeVisitor):
    def __init__(self):
        self.fileName = None
        self.defmagic = set()
        self.usedmagic = set()
        self.subscriptnodes = [] #avoid replicate node code smell reports
        self.containernodes = [] #avoid replicate node code smell reports
        self.messagenodes = [] #avoid replicate node code smell reports
        self.scopenodes = []
        self.imports = set()
        self.result = []

    def count_lines(self,node):
        childnodes = list(ast.walk(node))
        lines = set()
        for n in childnodes:
          if hasattr(n,'lineno'):
            lines.add(n.lineno)
        return len(lines)

    def visit_Lambda(self,node):
        expr = astunparse.unparse(node)
        exprLength = len(expr.strip()) - expr.count(' ') - 2
        par = len(node.args.args)
        noo = 0
        type_filters = [_ast.Load,_ast.Store,_ast.Del,_ast.AugLoad,_ast.AugStore,_ast.Param,
        _ast.Ellipsis,_ast.ExtSlice,_ast.Index,_ast.And,_ast.Or,
        _ast.Add,_ast.Sub,_ast.Mult,_ast.Div,_ast.Mod,_ast.Pow,_ast.LShift,
        _ast.RShift,_ast.BitOr,_ast.BitXor,_ast.BitAnd,_ast.FloorDiv,
        _ast.Invert,_ast.Not,_ast.UAdd,_ast.USub,
        _ast.Eq,_ast.NotEq,_ast.Lt,_ast.LtE,_ast.Gt,_ast.GtE,_ast.Is,_ast.IsNot,_ast.In,_ast.NotIn,
        _ast.comprehension,_ast.ExceptHandler,_ast.arguments,_ast.keyword,_ast.alias ]
        for i in ast.walk(node.body):
            if type(i) not in type_filters:
                noo = noo + 1
        self.result.append((9,self.fileName,node.lineno,exprLength,par,noo))
        self.generic_visit(node) 

    def visit_TryExcept(self,node):
        exceptions = ["BaseException","Exception","StandardError"]
        i = len(node.handlers)
        for item in node.handlers:
            i = i-1
            if i!=0 and astunparse.unparse(item.body[0]).strip() == "pass":
                self.result.append((7,self.fileName,node.lineno,'pass'))
                self.generic_visit(node) 
                return
            if item.type is not None:
                if isinstance(item.type,_ast.Tuple) or isinstance(item.type,_ast.List):
                    for e in item.type.elts:
                        if hasattr(e,"id") and e.id in exceptions:
                            self.result.append((7,self.fileName,node.lineno,'genrallist'))
                            self.generic_visit(node) 
                            return
                elif i!=0 and hasattr(item.type,"id") and item.type.id in exceptions:
                    self.result.append((7,self.fileName,node.lineno,'general'))
                    self.generic_visit(node) 
                    return
            elif i!=0:
              self.result.append((7,self.fileName,node.lineno,'general'))
              self.generic_visit(node)
              return

    def visit_ClassDef(self,node):
      # baseClassesSize
      className = node.name
      baseClassesSize = len(node.bases)
      if baseClassesSize>0:
        self.result.append((4,self.fileName,node.lineno,baseClassesSize))
      lines = set()
      res = [node]
      while len(res) >= 1:
        t = res[0]
        for n in ast.iter_child_nodes(t):
          if not hasattr(n,'lineno') or ((isinstance(t,_ast.FunctionDef) or isinstance(t,_ast.ClassDef)) and n == t.body[0] and isinstance(n,_ast.Expr)):
            continue
          lines.add(n.lineno)
          if isinstance(n,_ast.ClassDef) or isinstance(n,_ast.FunctionDef):
            continue
          else:
            res.append(n)
        del res[0]
      self.result.append((5,self.fileName,node.lineno,len(lines)))
      self.generic_visit(node)

    def visit_FunctionDef(self,node):
      # argsCount
      def findCharacter(s,d):
        try:
          value = s.index(d)
        except ValueError:
          return -1
        else:
          return value
      funcName = node.name.strip()
      p = re.compile("^(__[a-zA-Z0-9]+__)$")
      if p.match(funcName.strip()) and funcName != "__import__" and funcName != "__all__":
        self.defmagic.add((funcName,self.fileName,node.lineno))
      stmt = astunparse.unparse(node.args)
      arguments = stmt.split(",")
      argsCount = 0
      for element in arguments:
        if findCharacter(element,'=') == -1:
          argsCount += 1
      self.result.append((1,self.fileName,node.lineno,argsCount))
      #function length
      lines = set()
      res = [node]
      while len(res) >= 1:
        t = res[0]
        for n in ast.iter_child_nodes(t):
          if not hasattr(n,'lineno') or ((isinstance(t,_ast.FunctionDef) or isinstance(t,_ast.ClassDef)) and n == t.body[0] and isinstance(n,_ast.Expr)):
            continue
          lines.add(n.lineno)
          if isinstance(n,_ast.ClassDef) or isinstance(n,_ast.FunctionDef):
            continue
          else:
            res.append(n)
        del res[0]
      self.result.append((2,self.fileName,node.lineno,len(lines))) 
      #nested scope depth
      if node in self.scopenodes:
        self.scopenodes.remove(node)
        self.generic_visit(node)
        return
      dep = [[node,1]] #node,nestedlevel
      maxlevel = 1
      while len(dep) >= 1:
        t = dep[0][0]
        currentlevel = dep[0][1]
        for n in ast.iter_child_nodes(t):
          if isinstance(n,_ast.FunctionDef):
            self.scopenodes.append(n)
            dep.append([n,currentlevel+1])
        maxlevel = max(maxlevel,currentlevel)
        del dep[0]
      if maxlevel>1:
        self.result.append((3,self.fileName,node.lineno,maxlevel)) #DOC
      self.generic_visit(node) 

    def visit_Call(self,node):
      funcName = astunparse.unparse(node.func).strip()
      p = re.compile("^(__[a-zA-Z0-9]+__)$")
      if p.match(funcName) and funcName != "__import__" and funcName != "__all__":
        self.usedmagic.add((funcName,self.fileName,node.lineno))
      self.generic_visit(node)

    def visit_ListComp(self,node):
        count = 0
        expr = astunparse.unparse(node)
        exprLength = len(expr.strip()) - expr.count(' ')
        for item in expr.split(" "):
            if item.strip() == "if" or item.strip() == "for":
                count += 1
        noo = -1
        type_filters = [_ast.Load,_ast.Store,_ast.Del,_ast.AugLoad,_ast.AugStore,_ast.Param,
        _ast.Ellipsis,_ast.ExtSlice,_ast.Index,_ast.And,_ast.Or,
        _ast.Add,_ast.Sub,_ast.Mult,_ast.Div,_ast.Mod,_ast.Pow,_ast.LShift,
        _ast.RShift,_ast.BitOr,_ast.BitXor,_ast.BitAnd,_ast.FloorDiv,
        _ast.Invert,_ast.Not,_ast.UAdd,_ast.USub,
        _ast.Eq,_ast.NotEq,_ast.Lt,_ast.LtE,_ast.Gt,_ast.GtE,_ast.Is,_ast.IsNot,_ast.In,_ast.NotIn,
        _ast.comprehension,_ast.ExceptHandler,_ast.arguments,_ast.keyword,_ast.alias ]
        for i in ast.walk(node):
            if type(i) not in type_filters:
                noo = noo + 1
        self.result.append((11,self.fileName,node.lineno,exprLength,count,noo))
        self.generic_visit(node)  
           
    def visit_SetComp(self,node):
        self.visit_ListComp(node)

    def visit_DictComp(self,node):
        self.visit_ListComp(node)

    def visit_GeneratorExp(self,node):
        self.visit_ListComp(node)

    def visit_IfExp(self,node):
      expr = astunparse.unparse(node)
      exprLength = len(expr.strip()) - expr.count(' ') - 2
      childnodes = list(ast.walk(node))
      lines = 0
      for n in childnodes:
        if hasattr(n,'lineno'):
          lines = max(n.lineno-node.lineno,lines)
      lines = lines + 1
      self.result.append((10,self.fileName,node.lineno,exprLength,lines))
      self.generic_visit(node) 

    def visit_Subscript(self,node):
      if node in self.subscriptnodes:
        self.subscriptnodes.remove(node)
        self.generic_visit(node)
        return
      maxcount = 1
      t = node
      while True:
        if isinstance(t.value,_ast.Subscript):
          self.subscriptnodes.append(t.value)
          maxcount = maxcount + 1
          t = t.value
        else:
          break
      self.result.append((6,self.fileName,node.lineno,maxcount)) #LEC
      self.generic_visit(node) 

    def visit_List(self,node):
      if node in self.containernodes:
        self.containernodes.remove(node)
        self.generic_visit(node)
        return
      res = [[node,1]] #node,nestedlevel,type
      maxlevel = 1
      maxtype = 0
      while len(res) >= 1:
        t = res[0][0]
        currentlevel = res[0][1]
        if type(t) in [_ast.Tuple,_ast.List,_ast.Set,_ast.Dict]:
          childnodes = t.keys if isinstance(t,_ast.Dict) else t.elts
          for n in childnodes:
            if type(n) in [_ast.Tuple,_ast.Dict,_ast.List,_ast.Set]:
              self.containernodes.append(n)
              if type(n) not in res[0]:
                res[0].append(type(n))
              res.append([n,currentlevel+1])
        maxlevel = max(maxlevel,currentlevel)
        maxtype = max(maxtype,len(res[0])-2)
        del res[0]
        if isinstance(t,_ast.Dict):
          childnodes = t.values
          valuestype = set()
          for n in childnodes:
            if type(n) in [_ast.Tuple,_ast.Dict,_ast.List,_ast.Set]:
              self.containernodes.append(n)
              valuestype.add(type(n))
              res.append([n,currentlevel+1])
          maxtype = max(maxtype,len(valuestype))
      if maxlevel>1 or maxtype>0:
        self.result.append((6,self.fileName,node.lineno,maxlevel,maxtype)) #DNC,NCT
      self.generic_visit(node)

    def visit_Tuple(self,node):
      self.visit_List(node)

    def visit_Dict(self,node):
      self.visit_List(node)

    def visit_Set(self,node):
      self.visit_List(node) 

    def visit_Attribute(self,node):
      if node in self.messagenodes:
        self.messagenodes.remove(node)
        self.generic_visit(node)
        return
      maxcount = 1
      t = node
      while True:
        if isinstance(t.value,_ast.Attribute):
          self.messagenodes.append(t.value)
          maxcount = maxcount + 1
          t = t.value
        else:
          break
      if maxcount>1:
        self.result.append((13,self.fileName,node.lineno,maxcount)) #LMC
      self.generic_visit(node)

    def visit_Import(self,node):
      if self.fileName[-12:] == '\\__init__.py':
        self.generic_visit(node)
        return
      for alias in node.names:
        if len(alias.name)>4 and alias.name[0:2] == '__' and alias.name[-2:] == '__':
            continue
        if alias.asname is not None:
          for (name,file,lineno) in self.imports:
            if name==alias.asname and self.fileName==file:
              break
          else:
            self.imports.add((alias.asname,self.fileName,node.lineno))
        elif alias.name != '*':
          for (name,file,lineno) in self.imports:
            if name==alias.name and self.fileName==file:
              break
          else:
            self.imports.add((alias.name,self.fileName,node.lineno))
      self.generic_visit(node)

    def visit_ImportFrom(self,node):
      if self.fileName[-12:] == '\\__init__.py':
        self.generic_visit(node)
        return
      try:
        if node.module is not None and len(node.module)>4 and node.module[0:2] == '__' and node.module[-2:] == '__':
          self.generic_visit(node)
          return
      except:
        print astunparse.unparse(node)
      for alias in node.names:
        if len(alias.name)>4 and alias.name[0:2] == '__' and alias.name[-2:] == '__':
            continue
        if alias.asname is not None:
          for (name,file,lineno) in self.imports:
            if name==alias.asname and self.fileName==file:
              break
          else:
            self.imports.add((alias.asname,self.fileName,node.lineno))
        elif alias.name != '*':
          for (name,file,lineno) in self.imports:
            if name==alias.name and self.fileName==file:
              break
          else:
            self.imports.add((alias.name,self.fileName,node.lineno))
      self.generic_visit(node)

if __name__ == '__main__':
    pass