#### saros
mini program that links revisions in a document repository.

see saros.py for detailed description of saros.

this is an excercise in OO programming.  guidelines followed:
  1. no more than one '.' per line, meaning avoid code such as:
       - in class A -> `B.some_method().do_something()`
       - in class A -> ```var = B.some.method()
                          C.another_method(var)```
                     
  2. avoid calling some object's method in a loop with the same instance:
       - In class A -> ```for each some_container:
                            b.some_method(each)```
                        
  3. Avoid long chain of parameter passing:
       - in class A -> ```B.some_method(var)```
       - in class B -> ```C.another_method(var)```
      
to run the program:
  - cd to directory where this README file is
  - type below command & press ENTER:

      - python saros.py

  - you should see the output on the screen


