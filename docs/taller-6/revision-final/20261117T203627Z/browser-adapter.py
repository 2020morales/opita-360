# Execute the existing verifier with isolated output and current base metadata.
from pathlib import Path

root = Path(__file__).resolve().parents[4]
source = root / "docs/taller-4/verificar.py"
output = Path(__file__).resolve().parent / "browser"
text = source.read_text(encoding="utf-8")
old = "OUT = Path(__file__).resolve().parent / 'evidencias'"
assert text.count(old) == 1
text = text.replace(old, "OUT = Path(" + repr(str(output)) + ")")
text = text.replace("'base':'d81614d'", "'base':'8cce952'")
exec(compile(text, str(source), "exec"), {"__file__": str(source), "__name__": "__main__"})
