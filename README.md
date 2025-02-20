# SugangManager
수강신청 자동 모니터링 및 신청 프로그램. 주기적으로 원하는 강의 중 빈 강의가 있나 확인 후, 잔여 좌석이 있으면 자동으로 신청.

## Installation
```bash
conda create -n sugang python=3.10
conda activate sugang
pip install -r requirements.txt
```

## Run Manager
```bash
python main.py --id <학번> --pw <비밀번호> --grade <학년> --to_integrate <티통 여부> --classes <들을 수업들 학수번호>
```

### Args

| 인자명            | 타입        | 설명                                             | 예시 값                  |
|------------------|-------------|--------------------------------------------------|-------------------------|
| `--id`           | `str`       | 학번                                              | `2022123456`            |
| `--pw`           | `str`       | 비밀번호                                          | `mypassword`            |
| `--grade`        | `int`       | 학년 (1~4)                                        | `3`                     |
| `--to_integrate` | `bool`      | 티통 여부                                         | `True`                  |
| `--classes`      | `list[str]` | 신청할 강의의 학수번호-분반 (띄어쓰기로 구분)        | `GELT031-I1 ESM3074-41` |



