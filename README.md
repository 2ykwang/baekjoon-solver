## baekjoon-solver

백준 채점 도구

### Installation
```shell
$ pip install baekjoon_solver
```

### Usage

- `solve <filename> -p <problem_id>`

```shell
# ex)
$ solve test.py -p 11403

테스트 케이스 1
============================= 통과 0.024250507354736328s =============================
테스트 케이스 2
============================= 통과 0.02342987060546875s =============================
```

- `solve <filename>`

파일내용 상단에 문제 번호를 명시해야 함
```
test1.py

# problem: 1111 or
# 1111
```

```shell
# ex)
$ solve solve test1.py

테스트 케이스 1

        > 실행 값:
6
0
        > 예상 값:
3
0
============================= 실패 0.015842199325561523s =============================
```

### vscode integration

- Command palette (shift + ctrl + p) 열기
- Tasks: Configure Task 선택
- 아래 내용 입력

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Solver",
            "type": "shell",
            "command": "solve",
            "args": [
                "\"${file}\""
            ],
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": true,
                "showReuseMessage": false,
                "clear": true,
                "revealProblems": "never"
            },
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}
```

- shift + ctrl + b 를 눌러 사용


