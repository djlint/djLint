---
description: djLint 변경 내역입니다. 최근 릴리스의 업데이트와 다음 업그레이드에서 기대할 수 있는 기능을 확인하세요.
title: 변경 내역
keywords: 템플릿 린터, 템플릿 포맷터, djLint, HTML, 템플릿, 포맷터, 린터, 변경 내역
---

{% raw %}

# 변경 내역

이제 변경 내역은 [릴리스](https://github.com/djlint/djLint/releases)에 포함됩니다.

## 1.0.2

::: content

- 버그 수정 [#240](https://github.com/djlint/djLint/issues/240)
:::

## 1.0.1

::: content

- 버그 수정 [#236](https://github.com/djlint/djLint/issues/236)
:::

## 1.0.0

::: content

- 버그 수정 [#224](https://github.com/djlint/djLint/issues/224)
:::

## 0.7.6

::: content

- 버그 수정 [#189](https://github.com/djlint/djLint/issues/189), [#197](https://github.com/djlint/djLint/issues/197)
- 오류를 경고로 반환하는 `--warn` 플래그 추가
:::

## 0.7.5

::: content

- 버그 수정 [#187](https://github.com/djlint/djLint/issues/187)
- 템플릿 파일의 `yaml` 프런트 매터 지원 개선
- [#123](https://github.com/djlint/djLint/issues/123)에 따라 T032 규칙 추가
- [#124](https://github.com/djlint/djLint/issues/124)에 따라 H033 규칙 추가
- [#178](https://github.com/djlint/djLint/issues/178)에 따라 린터 프로필을 제외 방식에서 포함 방식으로 변경
- [#188](https://github.com/djlint/djLint/issues/188)에 따라 대체 구성 파일 옵션 `.djlintrc` 추가
:::

## 0.7.4

::: content

- 버그 수정 [#177](https://github.com/djlint/djLint/issues/177)
:::

## 0.7.3

::: content

- 버그 수정 [#173](https://github.com/djlint/djLint/issues/173), [#174](https://github.com/djlint/djLint/issues/174)
- `pyproject.toml`에서 Py3.6 지원 제외
:::

## 0.7.2

::: content

- 버그 수정 [#167](https://github.com/djlint/djLint/issues/167), [#166](https://github.com/djlint/djLint/issues/166), [#171](https://github.com/djlint/djLint/issues/171), [#169](https://github.com/djlint/djLint/issues/169)
:::

## 0.7.1

::: content

- 버그 수정 [#166](https://github.com/djlint/djLint/issues/166)
:::

## 0.7.0

::: content

- 사용자 정의 HTML 태그 구성 추가
- 버그 수정
:::

## 0.6.9

::: content

- HTML 및 Angular 프로필 추가
- #H023 규칙에서 일부 엔티티 허용
- 버그 수정
:::

## 0.6.8

::: content

- 버그 수정
- 문서 업데이트
:::

## 0.6.7

::: content

- 속성 안의 템플릿 태그를 포맷하는 옵트인 구성 옵션 `format_attribute_template_tags` 추가
- 린터 메시지의 변수 순서를 바꾸는 구성 옵션 `linter_output_format` 추가
- meta 태그를 검사하는 H030, H031 규칙 추가
:::

## 0.6.6

::: content

- 버그 수정
:::

## 0.6.5

::: content

- 출력 경로를 프로젝트 루트 기준 상대 경로로 변경
- 버그 수정
:::

## 0.6.4

::: content

- 버그 수정
:::

## 0.6.3

::: content

- django `blocktrans` 태그 지원 추가
- 버그 수정
:::

## 0.6.2

::: content

- 버그 수정
:::

## 0.6.1

::: content

- 버그 수정
- T028 규칙을 더 엄격하게 하고 메시지를 더 명확하게 변경
:::

## 0.6.0

::: content

- 템플릿 구문에서 닫히지 않은 문자열을 검사하는 T027 규칙 추가
- 속성 안에서 공백 제거 태그가 빠졌는지 검사하는 T028 규칙 추가
- form의 method가 소문자인지 검사하는 H029 규칙 추가
- "trimmed"가 없는 django blocktranslate 태그를 포맷 대상에서 제외
- 버그 수정
:::

## 0.5.9a

::: content

- python 3.10 테스트 지원 추가
- pre-commit 훅 추가
:::

## 0.5.9

::: content

- 제외 경로를 확장하는 `--use-gitignore` 옵션 추가
- 기본 제외 경로 매칭 방식 변경
- windows 제외 경로 수정
- 속성 안의 `{%...%}` 태그 포맷 수정
- 속성 안의 for 루프와 중첩 조건 포맷 수정
:::

## 0.5.8

::: content

- require_pragma 옵션 추가
- DJ018이 input의 `data-src`와 `action`도 잡아내도록 업데이트
- 인라인 무시 구문 수정
- 기본 사용법의 자리 표시자로 `--lint` 옵션 추가
- 버그 수정
:::

## 0.5.7

::: content

- 버그 수정
:::

## 0.5.6

::: content

- 비어 있는 id와 class 속성을 찾는 H026 규칙 추가
- 버그 수정
:::

## 0.5.5

::: content

- 설정을 통합하고 코드를 간소화
- 버그 수정
:::

## 0.5.4

::: content

- 빈 태그 쌍을 찾는 H020 규칙 추가
- 인라인 스타일을 찾는 H021 규칙 추가
- http 링크를 찾는 H022 규칙 추가
- 엔티티 참조를 찾는 H023 규칙 추가
- script와 style의 type을 찾는 H024 규칙 추가
- 짝 없는 태그를 검사하는 H025 규칙 추가. https://stackoverflow.com/a/1736801/10265880 에 감사드립니다
- 속성 포맷 개선
- `blank_line_after_tag` 옵션이 위치에 관계없이 줄바꿈을 추가하도록 업데이트
- django `trans` 태그 포맷 수정
- 인라인 스타일 포맷 추가
- 속성 안의 템플릿 조건 포맷 추가
- 린터 규칙에서 URL이 올 수 있는 위치로 srcset 추가
- 포맷 속도 향상
- [jayvdb](https://github.com/jayvdb)에게 특별히 감사드립니다
:::

## 0.5.3

::: content

- `--reformat/check` 옵션의 stdout 출력을, stdin을 입력으로 사용할 때만 새 HTML을 출력하도록 변경
:::

## 0.5.2

::: content

- `alt` 요구 사항을 H006에서 H013으로 분리
- 선택적인 사용자 정의 규칙 파일 추가
- 프로필 옵션으로 `golang` 추가
- 인라인 주석이 있는 무시 블록의 포맷 수정
- `--indent`와 `-e` 옵션에 기본 텍스트 추가
- URL 규칙이 #을 허용하도록 업데이트
- Windows OS에서의 파일 인코딩 수정
- 한 줄 템플릿 태그 정규식 수정
- 앞에 공백이 있는 태그에서 `blank_line_after_tag` 수정
:::

## 0.5.1

::: content

- H019 규칙 추가
- DJ018과 H012의 버그 수정
:::

## 0.5.0

::: content

- 린터 규칙의 여러 정규식 매칭 버그 수정
- 무시 블록에서 린터가 오류를 반환하지 않도록 변경
- `{% djlint:off %}...{% djlint:on %}` 태그로 코드 블록을 린터/포맷터에서 무시하는 옵션 추가
:::

## 0.4.9

::: content

- 버그 [#35](https://github.com/djlint/djLint/issues/35) 수정
:::

## 0.4.8

::: content

- 버그 [#34](https://github.com/djlint/djLint/issues/34) 수정
:::

## 0.4.7

::: content

- `source` 태그를 한 줄 태그로 이동
:::

## 0.4.6

::: content

- 버그 [#31](https://github.com/djlint/djLint/issues/31) 수정
:::

## 0.4.5

::: content

- 문서에 모범 사례 추가
- 기본 린터/포맷터 규칙을 설정하는 `--profile` 옵션 추가
- jinja URL 패턴에 대한 린터 규칙 추가
:::

## 0.4.4

::: content

- 들여쓰기 구성을 문자열에서 정수로 변경. `--indent 3`
:::

## 0.4.3

::: content

- 들여쓰기 간격에 대한 CLI 옵션 추가. `--indent=" "`
:::

## 0.4.2

::: content

- `blank_line_after_tag` 옵션으로 태그 뒤에 공백을 추가하는 기능 지원
:::

## 0.4.1

::: content

- 여러 파일이나 폴더를 한 번에 처리하는 기능 지원
:::

## 0.4.0

::: content

- django `{# ... #}` 태그 포맷 수정
- figcaption, details, summary 태그의 들여쓰기 지원 추가
- `pyproject.toml`에서 제외 경로 목록을 재정의하거나 확장하는 기능 지원
:::

## 0.3.9

::: content

- 속성 처리 업데이트
:::

## 0.3.8

::: content

- stdin 지원 추가
:::

## 0.3.7

::: content

- `small`, `dt`, `dd` 태그의 포맷 수정
:::

## 0.3.6

::: content

- Nunjucks의 `{%-` 여는 블록에 대한 포맷터 지원 추가
:::

## 0.3.5

::: content

- 더 많은 Django 블록 지원 추가
- 사용자 정의 블록 지원 추가
- `pyproject.toml`의 구성 지원 추가
:::

## 0.3.4

::: content

- Nunjucks 공백 제거 태그 `-%}`의 포맷 수정
:::

## 0.3.3

::: content

- 짧은 `div` 태그를 한 줄로 둘 수 있도록 허용
:::

## 0.3.2

::: content

- Django 주석 포맷 수정
- textarea를 포맷 대상에서 제외
:::

## 0.3.1

::: content

- 속성 포맷 정규식 업데이트
- 린트 규칙 W010 업데이트
:::

## 0.3.0

::: content

- 포맷 변경 사항이 있으면 종료 코드를 1로 변경
- Jinja `asset` 태그 지원 추가
:::

## 0.2.9

::: content

- W018 정규식 업데이트
- 중복된 린트 메시지 제거
- Handlebars용 E001 업데이트
:::

## 0.2.8

::: content

- 이전 Click 버전에서 발생하는 진행률 표시줄 오류 수정
:::

{% endraw %}
