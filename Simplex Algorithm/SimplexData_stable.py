from abc import ABC, abstractmethod
import string
from typing import List, Self


class IoInterface(ABC):
    @abstractmethod
    def input(self):
        pass
    @abstractmethod
    def display(self):
        pass
    
class SimplexDataElement(IoInterface):
    def __init__(self, name,inputEquation=None,slackVariables=0):
        self.name=name
        self.inputEquation=inputEquation
        self.data=None
        self.slackVariables=slackVariables
    def input(self,inputEquation=None):
        inputEquation = inputEquation if inputEquation is not None else self.inputEquation
        if inputEquation is not None:
            # If inputEquation is provided, set self.data directly
            self.data = inputEquation
            self.n = len(self.data)  # Set the number of elements based on the provided data
        else:
            print("please write "+self.name)
            self.n=int(input("Enter number of elements (eg: x1, x2, x3 and the result. When one of the factors is 0 please write a 0):2x1+0x2-1x3<=22 means 4 elements: "))
            self.data=list(map(int,input("\nEnter the numbers with one space between them (eg: 2x1+0x2-1x3<=22: 2 0 -1 22):").strip().split()))[:self.n]
    def display(self):
        print(self.data)
        
class SimplexDataComposite(IoInterface):
    def __init__(self,name):
        self.name=name
        self.children=[]
    def add(self,component:IoInterface):
        self.children.append(component)
    def remove(self,component:IoInterface):
        self.children.remove(component)
    def input(self):
        for child in self.children:
            child.input()
    def display(self):
        for child in self.children:
            child.display()
    def format(self):
        newEquations = SimplexDataComposite('EquationsFormatted')
        slackNumber=1
        max_length=0
        for object in self.children:
            if isinstance(object,SimplexDataComposite):
                for equation in object.children:
                    if isinstance(equation,SimlexEquation):
                        formatted_data = equation.data[:-1] #copy
                        result=equation.data[-1]
                        slack_var = 1 if equation.smaller else -1
                        for i in range(slackNumber-1):
                            formatted_data.append(0)
                        formatted_data.append(slack_var)  # Append slack variable
                        formatted_data.append(result)
                        newEquation = SimlexEquation(equation.name + '_formatted', formatted_data, True)
                        newEquations.add(newEquation)
                        max_length = max(max_length, len(formatted_data))
                        slackNumber+=1
                newEquations.input()
        for child in newEquations.children:
            if isinstance(child, SimlexEquation):
                # Calculate how many zeros to append to reach max_length
                while len(child.data) < max_length:
                    child.data.insert(-1, 0)
                    child.slackVariables=slackNumber-1
        return newEquations
    
class SimplexTable(SimplexDataComposite):
    def __init__(self, name):
        super().__init__(name)  # Initialize SimplexDataComposite
        self.slackVariables = 0
        self.objectiveFunction = []  # Initialize the objective function

    def addEquations(self, equations: SimplexDataComposite):
        for equation in equations.children:
            self.children.append(equation)
            self.slackVariables = max(self.slackVariables, equation.slackVariables)
    def remove(self,component:SimplexDataComposite):
        self.children.remove(component)

    def addObjective(self, objective):
        for i,element in enumerate(objective.data):
            self.objectiveFunction.append(-element)
        ##self.objectiveFunction = objective.data
        # Determine how many variables are present
        num_variables = len(self.objectiveFunction)  # Exclude the result
        # Append zeros for slack variables if needed
        if num_variables < len(self.children[1].data):
            self.objectiveFunction += [0] * (len(self.children[1].data) - num_variables)
    
    def solveSimplex(self,debug=False):
        SimplexIteration=0
        nextIteration = any(element < 0 for element in self.objectiveFunction[:-1])
        while nextIteration:
            
        # Find the pivot column (the column with the most positive coefficient in the objective function)
            pivotColumn = self.objectiveFunction.index(min(self.objectiveFunction[:-1]))  # Exclude the result
            # Find the pivot row using the minimum ratio test
            smallest_ratio = float('inf')
            pivotRow = -1

            for i, equation in enumerate(self.children):
                if equation.data[pivotColumn] > 0:  # Only consider positive entries
                    ratio = equation.data[-1] / equation.data[pivotColumn]
                    print(ratio)
                    if ratio < smallest_ratio:
                        smallest_ratio = ratio
                        pivotRow = i
            # If no valid pivot row was found, break
            if pivotColumn == -1:
                break
            pivot_element = self.children[pivotRow].data[pivotColumn]
            RowCopy=self.children[pivotRow].data[:]
            print(RowCopy)
            RowNew=[]
            print(pivot_element)
            for i in range(len(RowCopy)):
                RowNew.append(RowCopy[i]/pivot_element)
            self.children[pivotRow].data[:] = RowNew[:]
            if debug: self.display()
            for i,equation in enumerate(self.children):
                if i==pivotRow:
                    continue
                if equation.data[pivotColumn] ==0:
                    continue
                factor = equation.data[pivotColumn]/RowNew[pivotColumn]
                if debug: print(factor)
                for j in range(len(equation.data)):
                    equation.data[j] =equation.data[j]-factor*RowNew[j]
                    
                
                if debug: self.display()
            factor = self.objectiveFunction[pivotColumn]/RowNew[pivotColumn]
            if debug: print(factor)
            for j in range(len(self.objectiveFunction)):
                self.objectiveFunction[j] = self.objectiveFunction[j]-factor*RowNew[j]
            
            if debug: self.display()
            SimplexIteration+=1
            nextIteration = any(element < 0 for element in self.objectiveFunction[:-1])
            if SimplexIteration>10: break
            
            
            
            
            
    def display(self):
        print(f"Table: {self.name}")

        # Find the maximum number of decision variables for formatting
        max_vars = max(len(eq.data) - 1 for eq in self.children)  # -1 for the result
        # Create variable headers for decision variables and slack variables
        var_headers = [f"x{i + 1}" for i in range(max_vars - self.slackVariables)] \
                      + [f"s{i + 1}" for i in range(self.slackVariables)] \
                      + ["Result"]
        
        print(" | ".join(var_headers))
        print("-" * (len(" | ".join(var_headers))))  # Print a separator line
        
        # Print each equation
        for equation in self.children:
            factors = equation.data[:-1]  # All except the last element (the result)
            result = equation.data[-1]     # The last element (the result)
            factors_str = [str(factor) for factor in factors] + [str(result)]
            print(" | ".join(factors_str))

    
        factors = self.objectiveFunction  # All except the last element (the result)
        factors_str = [str(factor) for factor in factors]
        print(" | ".join(factors_str))
    
    
        


    
class SimlexEquation(SimplexDataElement):
    def __init__(self,name,inputEquation=None,smaller=None,slackVariables=0):
        SimplexDataElement.__init__(self, name,inputEquation,slackVariables)
        self.type = "equation"
        self.smaller=smaller
        self.slackVariables=slackVariables

    def input(self,inputEquation=None):
        super().input(inputEquation)
        self.equality()

    def equality(self):
        if self.smaller is None:
            sign = str(input("What is the relation? (<=,>=,=)"))
            if sign.lower()=="<=":
              self.smaller = True
            else:
                self.smaller = False

    def display(self):
        # printing the list using loop
        for i in range(len(self.data)-1):
            if i==0:
                print(str(self.data[i])+"*x"+str(i+1), end='')
            else:
                print("+"+str(self.data[i])+"*x"+str(i+1), end='')
        if self.smaller:
            print("<="+str(self.data[-1]))
        else:
            print(">="+str(self.data[-1]))

class SimplexObjective(SimplexDataElement):
    def __init__(self,name,inputEquation=None,maximise=None):
        SimplexDataElement.__init__(self, name,inputEquation)
        self.type = "objective"
        self.maximisation=maximise
    def input(self,inputEquation=None):
        super().input(inputEquation=inputEquation)
        self.maximise()
    def maximise(self):
        if self.maximisation is None:
            sign = str(input("Is it a maximisation Problem? (yes/no)"))
            if sign.lower()=="yes":
                self.maximisation = True
            else:
                self.maximisation = False
    def display(self):
        if self.maximisation:
            print("Maximise Z=",end='')
        else:
            print("Minimize Z=",end='')
        for i in range(len(self.data)):
            if i==0:
                print(str(self.data[i])+"*x"+str(i+1), end='')
            else:
                print("+"+str(self.data[i])+"*x"+str(i+1), end='')
        print()

## here you can just input the equation in the code. the objective is in the form 2x1-1x2+2=Z and it is a maximisation problem.
## the constraints are defined in the way of 2x1+1x2+0x3<=10. 

objective=SimplexObjective(name='objective',inputEquation=[3,2,4],maximise=True)
eq1=SimlexEquation(name='eq1',inputEquation=[3,2,5,18],smaller=True)
eq2=SimlexEquation(name='eq2',inputEquation=[4,2,3,16],smaller=True)
eq3=SimlexEquation(name='eq3',inputEquation=[2,1,1,4],smaller=False)

## The Inputs can be used in the console. It is important to note that it is way harder (in my opinion). The amount of elements in the data element need to be
## defined (in teh example above, it would be 3, in the constraints equations it would need to be 4). then the relation needs to be defined with a string (maximisation problem yes/no, greater or equal <=/>=)

##objective=SimplexObjective(name='objective')
##eq1=SimlexEquation(name='eq1')
##eq2=SimlexEquation(name='eq2')
##eq3=SimlexEquation(name='eq3')

equations=SimplexDataComposite('equations')
equations.add(eq1)
equations.add(eq2)
equations.add(eq3)
simplexdata=SimplexDataComposite('Data')
simplexdata.add(objective)
simplexdata.add(equations)

simplexdata.input()
simplexdata.display()
DataFormatted=simplexdata.format()
##DataFormatted.display()
SolveTable=SimplexTable(name="SolveTable")
SolveTable.addEquations(DataFormatted)
SolveTable.addObjective(objective)
SolveTable.display()
SolveTable.solveSimplex(debug=True)
SolveTable.display()