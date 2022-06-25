import argparse
import re
import subprocess
import time
from typing import List, Optional, Tuple

import httpx
from bs4 import BeautifulSoup as BS
from colorama import Fore, init

init(autoreset=True)


def _normalize_line(output):
    return "\n".join([line.strip() for line in output.splitlines()])


def _fetch_sample_data_from_baekjoon(problem_id: int) -> Tuple[str, str]:
    headers = {
        "Content-Type": "text/html",
        "User-Agent": "acmicpc solver",
    }
    url = f"https://www.acmicpc.net/problem/{problem_id}"

    response = httpx.get(url, headers=headers)
    bs = BS(response.text, "html.parser")
    data = bs.find_all("pre", {"class": "sampledata"})

    if len(data) < 1 or len(data) % 2 != 0:
        raise ValueError("문제를 가져올 수 없습니다.")

    for sample_input, sample_output in zip(*[iter(data)] * 2):
        yield sample_input.text, sample_output.text


def run_code(filename: str, input_lines: List[str]) -> str:
    to_bytes = bytes("\n".join(input_lines), "utf-8")

    # TODO: get python path
    output = subprocess.check_output(
        ["python3", filename],
        input=to_bytes,
    )
    return output.decode()


def _print_judge(index: int, result: str, answer: str, execution_timedelta):
    result = result.strip()
    answer = answer.strip()

    print(f"테스트 케이스 {index}")

    if result == answer:
        print(
            f"{Fore.GREEN}============================= 통과 {execution_timedelta}s ============================="
        )
    else:
        print(f"\t> 실행 값:\n{Fore.RED}{result}({len(result)})")
        print(f"\t> 예상 값:\n{answer}({len(answer)})")
        print(
            f"{Fore.RED}============================= 실패 {execution_timedelta}s ============================="
        )


def execution(filename, problem_id: Optional[int] = None, sample_data=None):

    if sample_data is None:
        sample_data = []

    if problem_id:
        sample_data.extend(_fetch_sample_data_from_baekjoon(problem_id))

    for index, (sample_input, sample_output) in enumerate(sample_data):
        time_start = time.time()
        try:
            output = run_code(filename, sample_input.splitlines())
            time_delta = time.time() - time_start

            # remove whitespace
            result = _normalize_line(output)
            sample_output = _normalize_line(sample_output)

            _print_judge(index + 1, result, sample_output, time_delta)

        except subprocess.CalledProcessError:
            print("스크립트를 실행할 수 없습니다. 오류를 확인하세요.")


def _try_parse_problem_id(filename: str) -> Optional[str]:
    with open(filename) as f:
        text = f.read()
        if text:
            try:
                return re.findall(r"#\s*(problem|solve|test|문제|):?\s*(\d*)", text)[0][1]
            except IndexError:
                pass
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="문제 파일 경로")
    parser.add_argument("-p", "--problem", help="문제 번호")
    args = parser.parse_args()

    problem_id = args.problem or _try_parse_problem_id(args.filename)

    # sample_data
    execution(args.filename, problem_id)
