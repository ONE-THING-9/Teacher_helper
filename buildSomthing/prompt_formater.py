from jinja2 import Template

def generate_final_prompt(input_text: str) -> str:
    """
    Given an input, return the final prompt.
    """
    # Here you can add any processing logic to generate the final prompt
    final_prompt = f"{input_text}"
    return final_prompt

def render_jinja_template(template_str: str, context: dict) -> str:
    """
    Given a Jinja template and a dictionary of key-value pairs, render the template with the keys and return the string.
    """
    template = Template(template_str)
    rendered_string = template.render(context)
    return rendered_string
