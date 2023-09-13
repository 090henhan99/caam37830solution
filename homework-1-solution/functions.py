"""
A library of functions
"""
import numpy as np
import matplotlib.pyplot as plt
import numbers
class AbstractFunction:
    """
    An abstract function class
    """

    def derivative(self):
        """
        returns another function f' which is the derivative of x
        """
        raise NotImplementedError("derivative")


    def __str__(self):
        return "AbstractFunction"


    def __repr__(self):
        return "AbstractFunction"


    def evaluate(self, x):
        """
        evaluate at x

        assumes x is a numeric value, or numpy array of values
        """
        raise NotImplementedError("evaluate")


    def __call__(self, x):
        """
        if x is another AbstractFunction, return the composition of functions

        if x is a string return a string that uses x as the indeterminate

        otherwise, evaluate function at a point x using evaluate
        """
        if isinstance(x, AbstractFunction):
            return Compose(self, x)
        elif isinstance(x, str):
            return self.__str__().format(x)
        else:
            return self.evaluate(x)


    # the rest of these methods will be implemented when we write the appropriate functions
    def __add__(self, other):
        """
        returns a new function expressing the sum of two functions
        """
        return Sum(self, other)


    def __mul__(self, other):
        """
        returns a new function expressing the product of two functions
        """
        return Product(self, other)


    def __neg__(self):
        return Scale(-1)(self)


    def __truediv__(self, other):
        return self * other**-1


    def __pow__(self, n):
        return Power(n)(self)


    def plot(self, vals=np.linspace(-1,1,100), **kwargs):
        """
        plots function on values
        pass kwargs to plotting function
        """
        if isinstance(vals,np.ndarray) or isinstance(vals,numbers.Numbers) \
            or isinstance(vals, np.number):
            return plt.plot(vals, self.evaluate(vals), **kwargs)
        else:
            raise TypeError("vals type error, not array or number")




class Polynomial(AbstractFunction):
    """
    polynomial c_n x^n + ... + c_1 x + c_0
    """

    def __init__(self, *args):
        """
        Polynomial(c_n ... c_0)

        Creates a polynomial
        c_n x^n + c_{n-1} x^{n-1} + ... + c_0
        """
        self.coeff = np.array(list(args))


    def __repr__(self):
        return "Polynomial{}".format(tuple(self.coeff))


    def __str__(self):
        """
        We'll create a string starting with leading term first

        there are a lot of branch conditions to make everything look pretty
        """
        s = ""
        deg = self.degree()
        for i, c in enumerate(self.coeff):
            if i < deg-1:
                if c == 0:
                    # don't print term at all
                    continue
                elif c == 1:
                    # supress coefficient
                    s = s + "({{0}})^{} + ".format(deg - i)
                else:
                    # print coefficient
                    s = s + "{}({{0}})^{} + ".format(c, deg - i)
            elif i == deg-1:
                # linear term
                if c == 0:
                    continue
                elif c == 1:
                    # suppress coefficient
                    s = s + "{0} + "
                else:
                    s = s + "{}({{0}}) + ".format(c)
            else:
                if c == 0 and len(s) > 0:
                    continue
                else:
                    # constant term
                    s = s + "{}".format(c)

        # handle possible trailing +
        if s[-3:] == " + ":
            s = s[:-3]

        return s


    def evaluate(self, x):
        """
        evaluate polynomial at x
        """
        if isinstance(x, numbers.Number):
            ret = 0
            for k, c in enumerate(reversed(self.coeff)):
                ret = ret + c * x**k
            return ret
        elif isinstance(x, np.ndarray):
            x = np.array(x)
            # use vandermonde matrix
            return np.vander(x, len(self.coeff)).dot(self.coeff)


    def derivative(self):
        if len(self.coeff) == 1:
            return Polynomial(0)
        return Polynomial(*(self.coeff[:-1] * np.array([n+1 for n in reversed(range(self.degree()))])))


    def degree(self):
        return len(self.coeff) - 1


    def __add__(self, other):
        """
        Polynomials are closed under addition - implement special rule
        """
        if isinstance(other, Polynomial):
            # add
            if self.degree() > other.degree():
                coeff = self.coeff
                coeff[-(other.degree() + 1):] += other.coeff
                return Polynomial(*coeff)
            else:
                coeff = other.coeff
                coeff[-(self.degree() + 1):] += self.coeff
                return Polynomial(*coeff)

        else:
            # do default add
            return super().__add__(other)


    def __mul__(self, other):
        """
        Polynomials are clused under multiplication - implement special rule
        """
        if isinstance(other, Polynomial):
            return Polynomial(*np.polymul(self.coeff, other.coeff))
        else:
            return super().__mul__(other)


class Affine(Polynomial):
    """
    affine function a * x + b
    """
    def __init__(self, a, b):
        super().__init__(a, b)

class Scale(Polynomial):
    def __init__(self,a):
        super().__init__(a,0)
        
class Constant(Polynomial):
    def __init__(self,c):
        super().__init__(c)
        
class Compose(AbstractFunction):
    def __init__(self, f, g):
        self.f = f
        self.g = g
    def evaluate(self, x):
        return self.f(self.g(x))
    def derivative(self):
        return super().derivative(self.f)(self.g) \
            * super().derivative(self.g)
    def __repr__(self):
        return "Compose({0}, {1})".format(self.f.__repr__(),self.g.__repr__())
    def __str__(self):
        return self.g.__str__().format("("+self.f.__str__()+")")
    
            
class Product(AbstractFunction):
    def __init__(self, f : AbstractFunction, g : AbstractFunction):
        self.f = f
        self.g = g
    def evaluate(self,x):
            return self.f.evaluate(x) * self.g.evaluate(x)
    def derivative(self):
        return self.f.derivative(self.g) * self.g.derivative()
    def __repr__(self):
        return "Product({0},{1})".format(self.f.__repr__(),self.g.__repr__())
    def __str__(self):
        return "({0})*({1})".format(self.f.__str__(),self.g.__str__())

class Sum(AbstractFunction):
    def __init__(self, f : AbstractFunction, g : AbstractFunction):
        self.f = f
        self.g = g
    def evaluate(self,x):
            return self.f.evaluate(x) + self.g.evaluate(x)
    def derivative(self):
        return self.f.derivative() + self.g.derivative()
    def __repr__(self):
        return "Sum({0},{1})".format(self.f.__repr__(),self.g.__repr__())
    def __str__(self):
        return "({0})+({1})".format(self.f.__str__(),self.g.__str__())

class Power(AbstractFunction):
    def __init__(self,n):
        self.n = n
    def derivative(self):
        return self.n * Power(self.n-1)
    def __repr__(self):
        return 'Power({0})'.format(self.n)
    def __str__(self):
        return "({{0}})^({n})".format(n = self.n)
    def evaluate(self,x):
        return np.power(x,self.n)
    
class Log(AbstractFunction):
    def derivative(self):
        return Power(-1)
    def __repr__(self):
        return 'log({0})'.format(self.n)
    def __str__(self):
        return "log({0})"
    def evaluate(self,x):
        return np.log(x)
    
class Exponential(AbstractFunction):
    def derivative(self):
        return Exponential()
    def __repr__(self):
        return 'exp()'
    def __str__(self):
        return "exp({0})"
    def evaluate(self,x):
        return np.exp(x)
    
class Sin(AbstractFunction):
    def derivative(self):
        return Cos()
    def __repr__(self):
        return 'sin()'
    def __str__(self):
        return "sin({0})"
    def evaluate(self,x):
        return np.sin(x)
     
class Cos(AbstractFunction):
    def derivate(self):
        return -Sin()
    def __repr__(self):
        return 'cos()'
    def __str__(self):
        return "cos({0})"
    def evaluate(self,x):
        return np.cos(x)
    
class Symbolic():
    def __init__(self,data):
        self.data = data
    def __str__(self):
        return self.data + "({0})"
    def __call__(self,x):
        if isinstance(x, Symbolic):
            return CompSymbolic(self, x)
        else:
            return "{0}({1})".format(self.data,x)
    def derivative(self):
        return Symbolic(self.data+"'")
    def __add__(self,other):
        return SumSymbolic(self,other)
    def __mul__(self,other):
        return ProdSymbolic(self,other)
    def __rmul__(self,other):
        return ProdSymbolic(other,self)
    def __neg__(self):
        return ScaleSymbolic(-1)(self)
    
    
class SumSymbolic(Symbolic):
    def __init__(self,A:Symbolic,B:Symbolic):
        self.A = A
        self.B = B
    def __str__(self):
        return "({stringA}+{stringB})".format(stringA=self.A,stringB=self.B)
    def __call__(self,x):
        if isinstance(x, Symbolic):
            return CompSymbolic(self, x)
        else:
            return "({stringA}+{stringB})".format(stringA=self.A,stringB=self.B).format(x)
    def derivative(self):
        return self.A.derivative()+self.B.derivative()

class ProdSymbolic(Symbolic):
    def __init__(self,A:Symbolic,B:Symbolic):
        self.A = A
        self.B = B
    def __str__(self):
        return "({stringA}*{stringB})".format(stringA=self.A,stringB=self.B) 
    def __call__(self,x):
        if isinstance(x, Symbolic):
            return CompSymbolic(self, x)
        else:
            return "({stringA}*{stringB})".format(stringA=self.A,stringB=self.B).format(x)
    def derivative(self):
        return self.A.derivative() * self.B \
            + self.A * self.B.derivative()

class CompSymbolic(Symbolic):
    def __init__(self,A:Symbolic, B:Symbolic):
        self.A = A
        self.B = B
    def __str__(self):
        return "{stringA}".format(stringA=self.A).format(self.B) 
    def __call__(self,x):
        if isinstance(x, Symbolic):
            return CompSymbolic(self, x)
        else:
            return "{stringA}".format(stringA=self.A).format(self.B).format(x)
    def derivative(self):
        return self.A.derivative()(self.B)*self.B.derivative()
"""
class PolySymbolic(Symbolic):
    
class PowerSymbolic(Symbolic):
 """   
class SinSymbolic(Symbolic):
    def __init__(self):
        super().__init__("sin")
    def derivative(self):
        return CosSymbolic()    

class CosSymbolic(Symbolic):
    def __init__(self):
        super().__init__("cos")
    def derivative(self):
        return -SinSymbolic()   
     
class ExpSymbolic(Symbolic):
    def __init__(self):
        super().__init__('exp')
    def derivative(self):
        return self
    
class ScaleSymbolic(Symbolic):
    def __init__(self,n):
        if n >= 0:
            super().__init__("{0}*".format(n))
        if n < 0:
            super().__init__("(-{0})*".format(-n))
        self.n = n
    def derivative(self):
        return ConstSymbolic(self.n)
    def __call__(self,other):
        if isinstance(other,Symbolic):
            return ConstSymbolic(self.n) * other
        else:
            return self.data.format(other)
    def __add__(self,other):
        if isinstance(other,ScaleSymbolic):
            return ScaleSymbolic(self.n+other.n)
        else:
            return super().__add__(self,other)
    
class ConstSymbolic(Symbolic):
    def __init__(self,n):
        self.data = '{0}'.format(n)
        self.n = n
    def __str__(self):
        return self.data
    def __call__(self,other):
        return self
    def derivative(self):
        return ConstSymbolic(0)
    
class PowerSymbolic(Symbolic):
    def __init__(self,n):
            self.data = 'Power({{0}},{0})'.format(n)
            self.n = n
    def __str__(self):
        return self.data
    def __call__(self,other):
        if isinstance(other,Symbolic):
            return CompSymbolic(self,other)
        else:
            return self.data.format(other)
    def derivative(self):
        return ConstSymbolic(self.n) * PowerSymbolic(self.n-1)
    