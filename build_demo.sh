# remove old wheels
rm -f docs/src/static/py/*
# build new wheels
poetry run pip wheel . -w docs/src/static/py
# rename wheels
cd docs/src/static/py
mv djlint* djlint-99-py3-none-any.whl
mv click* click-99-py3-none-any.whl
mv colorama* colorama-99-py3-none-any.whl
mv cssbeautifier* cssbeautifier-99-py3-none-any.whl
mv EditorConfig* EditorConfig-99-py3-none-any.whl
mv html_tag_names* html_tag_names-99-py3-none-any.whl
mv html_void_elements* html_void_elements-99-py3-none-any.whl
mv jsbeautifier* jsbeautifier-99-py3-none-any.whl
mv pathspec* pathspec-99-py3-none-any.whl
mv PyYAML* PyYAML-99-py3-none-any.whl
mv json5* json5-99-py3-none-any.whl
