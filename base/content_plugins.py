from fluent_contents.extensions import plugin_pool, ContentPlugin
from base.models import ImageItem


@plugin_pool.register
class ImagePlugin(ContentPlugin):
    model = ImageItem
    #render_template = "plugins/announcementblock.html"
    category = "Simple blocks"
