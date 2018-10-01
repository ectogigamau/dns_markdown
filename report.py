from jinja2 import FileSystemLoader, Environment
import os, codecs

def save(html_name, data, time):
	env = Environment(loader=FileSystemLoader(""))
	template = env.get_template('template.html')

	with codecs.open(html_name, "w",encoding='utf8') as f:
	    f.write(template.render(categories=data, time=time))