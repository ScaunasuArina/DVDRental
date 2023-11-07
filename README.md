# DVD Rental project

** Logging **
Logging file is located in ./Connection

** Generating cover report**
For coverage report we use "coverage" library.

Installation:
```
    >> python3 -m pip install coverage
```

Run tests:
```
    >> python -m coverage run -m unittest unit_testing_database.py
```

Generate report:
```
    >> python -m coverage report
    Name                                  Stmts   Miss  Cover
    ---------------------------------------------------------
    Database\Film.py                        142     26    82%
    Database\database_error_messages.py       4      0   100%
    response_util.py                          8      0   100%
    unit_testing_database.py                 32      0   100%
    ---------------------------------------------------------
    TOTAL                                   186     26    86%
```

Generate report in HTML format (found in ./htmlcov/):
```
    >> python -m coverage html
    Wrote HTML report to htmlcov\index.html
```
