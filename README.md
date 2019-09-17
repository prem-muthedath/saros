# Mini program that links revisions in a document repository.

An excercise in OO programming.  Guidelines followed:
  1. No more than one '.' per line, meaning avoid code such as:
       (a) In class A -> B.some_method().do_something()
       (b) In class A -> var = B.some.method()
                         C.another_method(var)
                     
  2. Avoid calling some object's method repeatedly in a loop with the same instance:
       In class A -> for each some_container:
                        b.some_method(each)
                        
  3. Avoid long chain of parameter passing:
       In class A -> B.some_method(var)
       In class B -> C.another_method(var)
       
