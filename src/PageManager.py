from jinja2 import Template

from src.classes.tag import Tag


def createCSS(name):
    css_path = 'css/output/' + name
    content = """ """
    with open(css_path, 'w') as output_file:
        output_file.write(content)

def createHTML(fileName):
    html_path_template = 'html/template/' + fileName + '.html'
    html_path = 'html/output/' + fileName + '.html'

    with open(html_path_template, 'r') as file:
        html_template = file.read()

    html_template = Template(html_template)
    # this is all the data included in the html file
    css_file_name = fileName + '.css'
    data = {
        "css_path" : css_file_name
    } # data not necessary here
    html_template.render(data)
    with open(html_path, 'w') as output_file:
        output_file.write(html_template)

    # ------------------- create CSS
    prompt = input('Do you want to generate a css file ? (if "No" the style will be in html file)')
    while prompt != 'No' or prompt != 'Yes' or prompt != 'no' or prompt != 'yes' or prompt != 'y' or prompt != 'n' or prompt != 'N' or prompt !=  'Y':
        prompt = input('Invalid answer, do you want to generate a css file ? (if "No" the style will be in html file)')
    if prompt == "Yes":
        createCSS(fileName)
    # ------------------- saving the template thanks to the object



