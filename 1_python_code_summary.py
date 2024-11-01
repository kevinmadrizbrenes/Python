# Python Reference Code: From Basics to Advanced Concepts

# -------------------
# Basic Syntax & Data Types
# -------------------

# Printing to the console
print("Hello, World!")  # Output text to the console

# Variable declaration and types
integer_example = 10  # Integer
float_example = 10.5  # Float
string_example = "Python"  # String
boolean_example = True  # Boolean

# Type checking
print(type(integer_example))  # <class 'int'>
print(type(float_example))  # <class 'float'>
print(type(string_example))  # <class 'str'>
print(type(boolean_example))  # <class 'bool'>

# Basic Arithmetic
addition = 5 + 3  # Addition: 8
subtraction = 5 - 3  # Subtraction: 2
multiplication = 5 * 3  # Multiplication: 15
division = 5 / 3  # Division: 1.666...
modulus = 5 % 3  # Modulus (remainder): 2
power = 5 ** 3  # Exponentiation: 125

# -------------------
# Data Structures
# -------------------

# Lists - Ordered, mutable collection
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")  # Adding an item
print(fruits)  # ['apple', 'banana', 'cherry', 'orange']

# Tuples - Ordered, immutable collection
coordinates = (10.0, 20.0)
print(coordinates[0])  # Accessing elements: 10.0

# Dictionaries - Key-value pairs, mutable
person = {"name": "John", "age": 30}
person["age"] = 31  # Modifying a value
print(person)  # {'name': 'John', 'age': 31}

# Sets - Unordered, no duplicate items
unique_numbers = {1, 2, 3, 3}  # Duplicate '3' will be removed
print(unique_numbers)  # {1, 2, 3}

# -------------------
# Conditionals and Loops
# -------------------

# If statements
x = 10
if x > 5:
    print("x is greater than 5")
elif x == 5:
    print("x is equal to 5")
else:
    print("x is less than 5")

# For loop
for fruit in fruits:
    print(fruit)

# While loop
count = 0
while count < 3:
    print("Counting:", count)
    count += 1


# -------------------
# Functions
# -------------------

# Defining a function
def greet(name):
    """This function greets the person passed in the name argument."""
    return f"Hello, {name}!"


print(greet("Alice"))  # Calling the function

# Lambda function
square = lambda x: x * x
print(square(5))  # 25

# -------------------
# Advanced Data Structures & Techniques
# -------------------

# List comprehension
squares = [x ** 2 for x in range(10)]  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Dictionary comprehension
squares_dict = {x: x ** 2 for x in range(10)}

# Generator expression
squares_gen = (x ** 2 for x in range(10))  # Lazy evaluation


# -------------------
# Classes & Object-Oriented Programming
# -------------------

class Animal:
    """A simple class to represent an animal."""

    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Sound!"


class Dog(Animal):
    """Dog class that inherits from Animal class."""

    def speak(self):
        return "Woof!"


dog = Dog("Buddy")
print(dog.speak())  # Output: Woof!

# -------------------
# Error Handling
# -------------------

try:
    result = 10 / 0
except ZeroDivisionError as e:
    print("Error:", e)
finally:
    print("This will always execute.")

# -------------------
# Advanced Functions
# -------------------

# Map, Filter, Reduce
from functools import reduce

numbers = [1, 2, 3, 4]
squared_numbers = list(map(lambda x: x * x, numbers))  # Squares each element
filtered_numbers = list(filter(lambda x: x % 2 == 0, numbers))  # Filters even numbers
sum_numbers = reduce(lambda x, y: x + y, numbers)  # Sums up elements
print(squared_numbers)
print(filtered_numbers)
print(sum_numbers)

# -------------------
# Working with Files
# -------------------

with open("example.txt", "w") as file:
    file.write("Hello, File!")  # Write to a file

with open("example.txt", "r") as file:
    content = file.read()  # Read from a file
    print(content)

# -------------------
# Modules and Packages
# -------------------

# Importing built-in module
import math

print(math.sqrt(16))  # 4.0

# Importing a specific function from a module
from math import pi

print(pi)  # 3.141592653589793


# -------------------
# Decorators
# -------------------

def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")

    return wrapper


@my_decorator
def say_hello():
    print("Hello!")


say_hello()

# -------------------
# Concurrency and Parallelism
# -------------------

# Threading example
import threading


def print_numbers():
    for i in range(5):
        print(i)


thread = threading.Thread(target=print_numbers)
thread.start()
thread.join()

# -------------------
# Asyncio for Asynchronous Programming
# -------------------

import asyncio


async def async_hello():
    print("Hello asynchronously!")
    await asyncio.sleep(1)
    print("Done with async task.")


# Run the async function
asyncio.run(async_hello())

# -------------------
# Using Libraries: Example with Requests
# -------------------

# You need to install requests with `pip install requests`
# import requests

# response = requests.get("https://api.github.com")
# print(response.status_code)

# -------------------
# End of Reference Code
# -------------------

print("Python reference code executed successfully.")
