## Set up environment
### download uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
### start virtual machine
uv pip install langgraph
uv venv --seed .venv
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
. .venv\Scripts\Activate.ps1

## Running
aiq run --config_file <path/to/config.yml> [--input uestion?" | --input_file <path/to/input.txt>]
aiq run --config_file "examples/simple/src/aiq_simple/configs/config.yml" --input "What is LangSmith?"
aiq run --config_file "examples/my_pace/src/my_pace/configs/config.yml" --input "What is LangSmith?"

aiq workflow create --workflow-dir examples my_pace