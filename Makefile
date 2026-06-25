.PHONY: run

run:
	.venv/Scripts/uvicorn.exe app.main:app --reload
