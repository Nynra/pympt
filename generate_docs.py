from pydoc_markdown.interfaces import Context
from pydoc_markdown.contrib.loaders.python import PythonLoader
from pydoc_markdown.contrib.renderers.markdown import MarkdownRenderer

context = Context(directory='.')
loader = PythonLoader(search_path=['src'])
renderer = MarkdownRenderer(render_module_header=False)

loader.init(context)
renderer.init(context)

modules = loader.load()
contents = renderer.render_to_string(modules)
with open('docs/index.md', 'w') as f:
    f.write(contents)