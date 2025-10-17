import os
import subprocess
from textwrap import dedent

# ----------------- RAW DATA -----------------
title = 'Approximation de ln(x) par des suites'
solutions = [
    {
        'objective': 'Prouver les inégalités $T(x) \\le 2T(\\sqrt{x})$ et $2S(\\sqrt{x}) \\le S(x)$ pour tout $x \\in [1, +\\infty[$.',
        'deps': [],
        'steps': [
            {'action': 'Substitution des définitions de $T(x)$ et $T(\\sqrt{x})$.', 'expr': '$T(x) \\le 2T(\\sqrt{x}) \\iff \\frac{x^2 - 1}{x^2 + 1} \\le 2 \\frac{x - 1}{x + 1}$'},
            {'action': 'Factorisation de $x^2-1$ et simplification pour $x > 1$.', 'expr': '$\\frac{(x-1)(x+1)}{x^2 + 1} \\le 2 \\frac{x - 1}{x + 1} \\iff \\frac{x+1}{x^2 + 1} \\le \\frac{2}{x + 1}$'},
            {'action': 'Réarrangement algébrique.', 'expr': '$(x+1)^2 \\le 2(x^2 + 1)$'},
            {'action': 'Développement et simplification.', 'expr': '$x^2 + 2x + 1 \\le 2x^2 + 2 \\iff 0 \\le x^2 - 2x + 1$'},
            {'action': 'Identité remarquable.', 'expr': '$0 \\le (x-1)^2$, ce qui est vrai pour tout $x \\in [1, +\\infty[$.'},
            {'action': 'Substitution des définitions de $S(x)$ et $S(\\sqrt{x})$.', 'expr': '$2S(\\sqrt{x}) \\le S(x) \\iff 2 \\frac{x - 1}{2\\sqrt{x}} \\le \\frac{x^2 - 1}{2x}$'},
            {'action': 'Simplification et factorisation de $x^2-1$.', 'expr': '$\\frac{x - 1}{\\sqrt{x}} \\le \\frac{(x-1)(x+1)}{2x}$'},
            {'action': 'Réarrangement algébrique pour $x > 1$.', 'expr': '$2x \\le \\sqrt{x}(x+1) \\iff 2\\sqrt{x} \\le x+1$'},
            {'action': 'Réarrangement.', 'expr': '$0 \\le x - 2\\sqrt{x} + 1$'},
            {'action': 'Identité remarquable.', 'expr': '$0 \\le (\\sqrt{x} - 1)^2$, ce qui est vrai pour tout $x \\in [1, +\\infty[$.'}
        ],
        'result': '$\\text{N/A}$'
    },
    # ... you can paste all other questions from your raw data here ...
]

# ----------------- LATEX GENERATION -----------------
def generate_latex(title, questions):
    body = [f"\\section*{{{title}}}"]

    for i, q in enumerate(questions, start=1):
        body.append(f"\\subsection*{{Question {i}: {q['objective']}}}")

        for j, step in enumerate(q['steps'], start=1):
            body.append(f"\\paragraph*{{Étape {j}:}} {step['action']}")
            body.append(f"\\[ {step['expr']} \\]")

        if 'result' in q and q['result']:
            body.append(f"\\paragraph*{{Résultat:}} {q['result']}")

    # Join body outside the f-string to avoid backslash issues
    body_text = "\n".join(body)

    latex_code = dedent(
        "\\documentclass[11pt,a4paper]{article}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage[T1]{fontenc}\n"
        "\\usepackage[french]{babel}\n"
        "\\usepackage{amsmath, amssymb}\n"
        "\\usepackage{geometry}\n"
        "\\geometry{margin=2cm}\n"
        "\\begin{document}\n"
        + body_text +
        "\n\\end{document}"
    )
    return latex_code

# ----------------- PDF EXPORT -----------------
def export_to_pdf(title, questions, output_name="output"):
    tex_file = f"{output_name}.tex"
    pdf_file = f"{output_name}.pdf"

    latex_code = generate_latex(title, questions)
    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(latex_code)

    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"LaTeX compilation failed: {e.stderr.decode()}")

    # Cleanup auxiliary files
    for ext in (".aux", ".log"):
        f = output_name + ext
        if os.path.exists(f):
            os.remove(f)

    return os.path.abspath(pdf_file)

# ----------------- MAIN -----------------
if __name__ == "__main__":
    pdf_path = export_to_pdf(title, solutions, output_name="lnx_approximation")
    print(f"✅ PDF generated: {pdf_path}")
