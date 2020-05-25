#### saros
Program to link document revisions in Saros, a fictitious document repository.

See `./saros/saros.py` for detailed description of Saros.

This is an excercise in OO programming.  Guidelines followed:
  1. No more than one '.' per line, meaning avoid code such as:
       - in `class A` -> `B.some_method().do_something()`
       - in `class A` ->
       ```
          var = B.some.method()
          C.another_method(var)
        ```

  2. Avoid calling some object's method in a loop with the same instance:
       - In `class A` ->
       ```
        for each in some_container:
             b.some_method(each)
        ```

  3. Avoid long chain of parameter passing:
       - in `class A` -> `B.some_method(var)`
       - in `class B` -> `C.another_method(var)`

To run the program:
  - You need python package `aenum`; install using `pip` if you don't have it.
  - `cd` to `saros` directory (where this `README` file is)
  - Type below command & press `ENTER`:

      - `python -m saros`

  - You should see the output on the screen


