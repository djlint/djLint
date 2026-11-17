---
title: "Python API"
description: "djLint API로 직접 작성한 Python 코드에서 템플릿을 포맷하고 린트하세요."
---

`djlint.api`는 Python 프로그램에서 텍스트를 포맷하고 린트하며, 명령줄과 같은 결과를 냅니다. 에디터, 빌드 도구를 비롯해 템플릿을 메모리에 들고 있는 모든 프로그램을 위한 모듈입니다. 패키지의 다른 부분은 어느 릴리스에서든 바뀔 수 있으므로 `djlint.settings`나 `djlint.lint` 대신 이 모듈을 사용하세요. [사용자 정의 규칙 예시](/ko/docs/linter/#python-모듈-규칙)가 임포트하는 헬퍼인 `djlint.lint.get_line`, `djlint.helpers.inside_ignored_rule`, `djlint.helpers.inside_ignored_linter_block`도 계속 동작합니다.

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', "templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", *, python_rules=True, on_warning=None, **options)`는 폴더 안의 파일에 적용되는 구성을 읽습니다. 명령줄이 처음 받은 경로에서 [그러듯](/ko/docs/configuration/) 폴더에서 위쪽으로 구성을 찾으며, 현재 디렉터리를 바꾸지는 않습니다.

옵션은 명령줄 옵션의 이름을 밑줄로 바꿔 쓰며, 동작도 명령줄과 같습니다. 지정한 값은 구성 파일보다 우선하고, `False`, 빈 문자열, 그리고 대부분의 옵션에서 `0`은 지정하지 않은 것으로 간주합니다. 경로는 `pathlib.Path`로 전달합니다.

구성을 읽는 데는 시간이 걸리므로, 구성을 읽어 온 파일이 바뀌지 않는 동안에는 결과를 보관해 두세요. 결과는 텍스트 개수에 상관없이 계속 쓸 수 있습니다.

`python_rules=False`를 지정하면 `python_module`이 있는 사용자 정의 규칙을 불러오지 않으므로, 신뢰하지 않는 프로젝트의 코드가 실행되지 않습니다. 이런 규칙의 이름은 `config.skipped_rules`에 들어 있습니다.

`on_warning`에 메시지를 받는 함수를 넘기면, 잘못 쓴 설정 이름이나 어떤 규칙에도 없는 규칙 코드처럼 설정에 관한 모든 경고를 그 함수가 받습니다. 지정하지 않으면 각 경고는 프로세스마다 한 번 stderr로 출력됩니다. 읽을 수 없는 구성 파일이나 유효하지 않은 값은 `click.UsageError`를 발생시킵니다.

## format_text

`format_text(config, text)`는 포맷된 텍스트를 반환합니다. 첫 줄이 CRLF로 끝나는 텍스트는 CRLF로, 그 밖의 텍스트는 LF로 돌려줍니다. `require_pragma`를 사용하면 프래그마가 없는 텍스트는 바뀌지 않은 채로 돌아옵니다. `indent`와 `max_line_length`는 `load_config`에 넘긴 폴더에 적용되는 `.editorconfig`에서 가져옵니다. 명령줄은 파일마다 그 경로에 따라 가져옵니다.

## lint_text

`lint_text(config, text, filename="-")`는 `Finding`의 리스트를 문서 순서대로 반환합니다. `per-file-ignores`는 `filename`과 대조합니다. `require_pragma`를 사용하면 프래그마가 없는 텍스트에는 검사 결과가 없습니다.

`Finding`은 다음 필드를 가진 네임드 튜플입니다.

- `code`: `H013`과 같은 규칙 코드입니다.
- `message`: 규칙이 전하는 메시지입니다.
- `match`: 찾아낸 텍스트의 앞부분으로, 최대 20자입니다.
- `line`, `column`: 검사 결과가 시작되는 위치입니다. 줄은 1부터, 열은 0부터 셉니다.
- `end_line`, `end_column`: 끝나는 위치의 바로 다음으로, 뒤쪽 줄에 있을 수도 있습니다.

열은 바이트나 UTF-16 코드 단위가 아니라 문자 단위로 셉니다.

## is_excluded

`is_excluded(config, path)`는 명령줄과 마찬가지로 `exclude`, `extend_exclude`, gitignore에 따라 파일이 제외되는지 알려 줍니다. `format_text`와 `lint_text`는 이를 직접 확인하지 않습니다.

## 규칙 모듈

사용자 정의 규칙의 `python_module`은 프로세스마다 한 번, 구성의 프로젝트 루트에서 임포트됩니다. 계속 실행되는 프로그램이 다른 프로젝트의 규칙을 읽으려면, 첫 프로젝트에서 임포트한 모든 것을 `sys.modules`에서 제거하고 그 프로젝트의 루트를 `sys.path` 끝에서 제거해야 합니다.
