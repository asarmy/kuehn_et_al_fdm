# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/asarmy/kuehn_et_al_fdm/blob/coverage-data-branch/htmlcov/index.html)

| Name                                                |    Stmts |     Miss |   Cover |   Missing |
|---------------------------------------------------- | -------: | -------: | ------: | --------: |
| src/kuehn\_et\_al\_fdm/\_\_init\_\_.py              |       10 |        0 |    100% |           |
| src/kuehn\_et\_al\_fdm/\_common\_args.py            |       35 |        4 |     89% |22, 157-159 |
| src/kuehn\_et\_al\_fdm/\_help.py                    |        2 |        1 |     50% |        50 |
| src/kuehn\_et\_al\_fdm/calc\_displ\_avg.py          |       31 |        7 |     77% |89-99, 103 |
| src/kuehn\_et\_al\_fdm/calc\_displ\_profile.py      |       35 |        9 |     74% |103-116, 120 |
| src/kuehn\_et\_al\_fdm/calc\_displ\_site.py         |       43 |       10 |     77% |127, 160-174, 178 |
| src/kuehn\_et\_al\_fdm/calc\_params.py              |       47 |       10 |     79% |107, 135-148, 152 |
| src/kuehn\_et\_al\_fdm/calc\_prob\_exceed.py        |       72 |       35 |     51% |21-75, 202, 206-215, 220, 244-261 |
| src/kuehn\_et\_al\_fdm/calc\_prob\_occur.py         |       40 |        8 |     80% |74, 123-130, 134 |
| src/kuehn\_et\_al\_fdm/load\_data.py                |       26 |        3 |     88% | 53, 57-58 |
| src/kuehn\_et\_al\_fdm/prediction\_functions.py     |       56 |        3 |     95% |153-154, 159 |
| src/kuehn\_et\_al\_fdm/transformation\_functions.py |       14 |        0 |    100% |           |
| src/kuehn\_et\_al\_fdm/utilities.py                 |       24 |        1 |     96% |        22 |
|                                           **TOTAL** |  **435** |   **91** | **79%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/asarmy/kuehn_et_al_fdm/coverage-data-branch/badge.svg)](https://htmlpreview.github.io/?https://github.com/asarmy/kuehn_et_al_fdm/blob/coverage-data-branch/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/asarmy/kuehn_et_al_fdm/coverage-data-branch/endpoint.json)](https://htmlpreview.github.io/?https://github.com/asarmy/kuehn_et_al_fdm/blob/coverage-data-branch/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fasarmy%2Fkuehn_et_al_fdm%2Fcoverage-data-branch%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/asarmy/kuehn_et_al_fdm/blob/coverage-data-branch/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.