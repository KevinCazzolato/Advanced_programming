#Cazzolato Kevin SM3201245
class EmptyStackException(Exception):
    pass


class Stack:

    def __init__(self):
        self.data = []

    def push(self, x):
        self.data.append(x)

    def pop(self):
        if not self.data:
            raise EmptyStackException
        res = self.data[-1]
        self.data = self.data[:-1]
        return res

    def __str__(self):
        return " ".join([str(s) for s in self.data])


class Expression:

    def __init__(self):
        self.__stack=Stack()

    @classmethod
    def from_program(cls, text, dispatch):
        expr = cls()
        expression = text.split()

        for element in expression:
            if element.isdigit():
                expr.__stack.push(Constant(int(element)))
            elif element in dispatch:
                operator = dispatch[element]
                args = []
                [args.append(expr.__stack.pop()) for _ in range(operator.arity)]
                expr.__stack.push(operator(args))
            else:
                expr.__stack.push(Variable(element))
        return expr

    def evaluate(self, env):   
        return self.__stack.pop().evaluate(env)
        

    def __str__(self):
        return str(self.__stack)


class MissingVariableException(Exception):
    pass

class Variable(Expression):

    def __init__(self, name):
        self.name = name
        self.value=None

    def evaluate(self, env):
        if str(self.name) in env:
            self.value=env[str(self.name)]
            return self.value
        else:
            raise MissingVariableException('variabile inesistente')

    def __str__(self):
        return self.name



class Constant(Expression):

    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value

    def __str__(self):
        return str(self.value)


class Operation(Expression):

    def __init__(self, args):
        self.args = args

    def evaluate(self, env):
        raise NotImplementedError()
    
    def op(self,*args):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()    
    
class prog2(Operation):
    arity = 2

    def evaluate(self, env):
        for element in self.args:
            res = element.evaluate(env)
        return res

    def __str__(self):
        return f"prog2({', '.join(map(str, self.args))})"


class prog3(Operation):
    arity = 3

    def evaluate(self, env):
        for element in self.args:
            res = element.evaluate(env)
        return res

    def __str__(self):
        return f"prog3({', '.join(map(str, self.args))})"


class prog4(Operation):
    arity = 4

    def evaluate(self, env):
        for element in self.args:
            res = element.evaluate(env)
        return res

    def __str__(self):
        return f"prog4({', '.join(map(str, self.args))})"

class If(Operation):
    arity=3
    def __init__(self, args):
        super().__init__(args)
        self.cond=self.args[0]
        self.x=self.args[1]
        self.y=self.args[2]

    def evaluate(self, env):
        if(self.cond.evaluate(env)==True):
            return self.x.evaluate(env)
        else:
            return self.y.evaluate(env)
        
    def __str__(self):
        return f"ifyes({self.args[1]})ifno({self.args[2]})"


class SetV(Operation):
    arity=3
    def __init__(self,args):
        super().__init__(args)
        self.expr=args[2]
        self.n= args[1]
        self.name= args[0]


    def evaluate(self, env):
        varname = str(self.name)
        env[varname][self.n.evaluate(env)] = self.expr.evaluate(env)
        return env[varname][int(self.args[1].evaluate(env))] 

    
    def __str__(self):
        return f"{self.name}[{self.n}]={self.expr}"
    
class For(Operation):
    arity=4
    def __init__(self, args):
        super().__init__(args)
    
    def evaluate(self, env):
        i=str(self.args[0])
        start=int(self.args[1].evaluate(env))
        end=int(self.args[2].evaluate(env))
        expr=self.args[3]
        for j in range(start,end,1): #per chiarezza aggiungo 1
            env[i]=j 
            expr.evaluate(env)

    def __str__(self):
        return f"for({self.args[0]} from {self.args[1]} to {self.args[2]}) evaluate({self.args[3]})"


class BinaryOp(Operation):
    arity = 2

    def __init__(self, args):
        super().__init__(args)
        (self.x, self.y) = self.args

    def evaluate(self, env):
        x=self.x.evaluate(env)
        y=self.y.evaluate(env)
        return self.op(x,y)
    
class defsub(BinaryOp):
    def evaluate(self, env):
        env[str(self.x)]=self.y
        
    def __str__(self):
        return f"def ({self.x})"

class While(BinaryOp):
    def evaluate(self, env):
        while(self.args[0].evaluate(env)):
            self.args[1].evaluate(env)

    def __str__(self):
        return f"while({self.x}) (evaluate({self.args[1]}))"

class Valloc(BinaryOp):
    def evaluate(self, env):
        #varname = str(self.args[0])
        varname=str(self.x)
        env[varname] = [0] * int(self.y.evaluate(env))
    
    def __str__(self):
        return f"valloc({str(self.x)})"

    

class Seteq(BinaryOp):
    def evaluate(self,env):
        env[str(self.x)] = self.y.evaluate(env)
        return env[str(self.x)]

    def __str__(self): 
        return f"({self.x} = {self.y})"



class Addition(BinaryOp):
    def op(self, x, y):
        return x+y
    
    def __str__(self):
        return f"({self.x} + {self.y})"


class Subtraction(BinaryOp):    
    def op(self, x, y):
        return x-y

    def __str__(self):
        return f"({self.x} - {self.y})"


class Division(BinaryOp):
    def op(self, x, y):
        if(y==0):
            raise ValueError("Division by zero")
        return x/y
    
    def __str__(self):
        return f"({self.x} / {self.y})"


class Multiplication(BinaryOp):
    def op(self, x, y):
        return x*y
    
    def __str__(self):
        return f"({self.x} * {self.y})"


class Power(BinaryOp):
    def op(self, x, y):
        return x**y

    def __str__(self):
        return f"({self.x} ** {self.y})"
    
class modul(BinaryOp):
    def op(self, x, y):
        return x % y
        
        
class Greater(BinaryOp):
    def op(self, x, y):
        return x>y
    
    def __str__(self):
        return f"({self.x} > {self.y})"
        
class GraterEqual(BinaryOp):
    def op(self, x, y):
        return x>=y
    
    def __str__(self):
        return f"({self.x} >= {self.y})"

class Less(BinaryOp):
    def op(self, x, y):
        return x<y

    def __str__(self):
        return f"({self.x} < {self.y})"
        
class LessEqual(BinaryOp):
    def op(self, x, y):
        return x<=y

    def __str__(self):
        return f"({self.x} <= {self.y})"

class Equal (BinaryOp):
    def op(self, x, y):
        return x==y

    def __str__(self):
        return f"({self.x} = {self.y})"

class NotEqual (BinaryOp):
    def op(self, x, y):
        return x!=y

    def __str__(self):
        return f"({self.x} != {self.y})"


    
class UnaryOp(Operation):
    arity = 1

    def __init__(self, args):
        super().__init__(args)
        self.x = args[0]

    def evaluate(self, env):
        x=self.x.evaluate(env)
        return self.op(x)

class Reciprocal(UnaryOp):
    def op(self, x):
        if x==0:
            raise ValueError("Reciprocal of zero")
        else:
            return 1/x

    def __str__(self):
        return f"(1 / {self.x})"


class AbsoluteValue(UnaryOp):
    def op(self, x):
        return abs(x)

    def __str__(self):
        return f"abs({self.x})"
    

class Alloc(UnaryOp):
    def evaluate(self, env):
        varname = str(self.x)
        env[varname] = 0 
    
    def __str__(self):
        return f"alloc({str(self.x)})"
    
class call(UnaryOp):
    def evaluate(self, env):
        return env[str(self.args[0])].evaluate(env)
    
    def __str__(self):
        return f"call({str(self.args[0])})"

class Print(UnaryOp):
    op="print"
    def evaluate(self, env):
        ris= self.args[0].evaluate(env)
        print(ris)
        return ris
    
    def __str__(self):
        return f"print({self.args[0]})"
    
class NoOp(Operation):
    arity=0
    def evaluate(self, env):
        pass
    def __str__(self):
        return f""


d = {"+": Addition, "*": Multiplication, "**": Power, "-": Subtraction,
     "/": Division, "1/": Reciprocal, "abs": AbsoluteValue, ">": Greater, ">=": GraterEqual,
     "<": Less, "<=": LessEqual, "=": Equal, "!=": NotEqual,"%": modul, "alloc": Alloc, "valloc": Valloc, "setq": Seteq, "setv": SetV, "if": If,
     "while": While, "for": For, "defsub": defsub, "print": Print, "nop": NoOp,"call":call, "prog2": prog2, "prog3": prog3, "prog4": prog4}


examples = list()
examples.append("2 3 + x * 6 5 - / abs 2 ** y 1/ + 1/")
examples.append("v print i i * i v setv prog2 10 0 i for 10 v valloc prog2")
examples.append("x print f call x alloc x 4 + x setq f defsub prog4")
examples.append("nop i print i x % 0 = if 1000 2 i for 783 x setq x alloc prog3")
examples.append("nop x print prime if nop 0 0 != prime setq i x % 0 = if 1 x - 2 i for 0 0 = prime setq prime alloc prog4 100 2 x for")
examples.append("v print i j * 1 i - 10 * 1 j - + v setv 11 1 j for 11 1 i for 100 v valloc prog3")
examples.append("x print 1 3 x * + x setq 2 x / x setq 2 x % 0 = if prog2 1 x != while 50 x setq x alloc prog3")
env={"x": 3, "y": 7}
e = Expression.from_program(examples[6], d)
print(e)
res = e.evaluate(env)
