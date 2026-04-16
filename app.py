import gradio as gr
from parser import Parser
from myToken import token
from simplifierLogic import simplify_full, to_string

def simplify_expression(expr_str):
    try:
        tokens = token(expr_str)
        parser = Parser(tokens)
        ast = parser.parse()
        simplified = simplify_full(ast)

        return (
            str(tokens),
            to_string(ast),
            to_string(simplified)
        )
    except Exception as e:
        return ("Error", "Error", str(e))

demo = gr.Interface(
    fn=simplify_expression,
    inputs=gr.Textbox(
        label="Boolean expression",
        placeholder="Example: (A+0)*(A+1)"
    ),
    outputs=[
        gr.Textbox(label="Tokens"),
        gr.Textbox(label="Parsed expression"),
        gr.Textbox(label="Simplified expression"),
    ],
    title="Boolean Simplifier",
    description="Enter a boolean algebra expression to parse and simplify."
)

if __name__ == "__main__":
    demo.launch()
