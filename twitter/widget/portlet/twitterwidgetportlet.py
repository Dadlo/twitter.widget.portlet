from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from twitter.widget.portlet import twitterWidgetPortletMessageFactory as _


class ItwitterWidgetPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    profile = schema.TextLine(title=_(u"Profile to be Searched"),
                                  description=_(u"Profile to be Searched"),
                                  required=False)
    tpinterval = schema.Int(title=_(u"Interval of Tweets"),
                                  description=_(u"Interval of Tweets to be loaded"),
                                  required=True,
                                  default=30000)
    tpwidth = schema.Int(title=_(u"Portlet Width"),
                                  description=_(u"Portlet Width"),
                                  required=True,
                                  default=250)
    tpheight = schema.Int(title=_(u"Portlet Height"),
                                  description=_(u"Portlet Height"),
                                  required=True,
                                  default=300)
    shellbackground = schema.ASCIILine(title=_(u"Shell Background"),
                                  description=_(u"Shell Background"),
                                  required=True,
                                  default="#feb200")
    shellfontcolor = schema.ASCIILine(title=_(u"Sheel Font Color"),
                                  description=_(u"Sheel Font Color"),
                                  required=True,
                                  default="#262626")
    tweetsbackground = schema.ASCIILine(title=_(u"Tweets Background"),
                                  description=_(u"Tweets Background"),
                                  required=True,
                                  default="#ffffff")
    tweetsfontcolor = schema.ASCIILine(title=_(u"Tweets Font Color"),
                                  description=_(u"Tweets Font Color"),
                                  required=True,
                                  default="#3d3d3d")
    tweetslinkscolor = schema.ASCIILine(title=_(u"Tweets Links Color"),
                                  description=_(u"Tweets Links Color"),
                                  required=True,
                                  default="#0c59cc")

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ItwitterWidgetPortlet)

    tpinterval = 30000
    tpwidth = 250
    tpheight = 300
    shellbackground = "#feb200"
    shellfontcolor = "#262626"
    tweetsbackground = "#ffffff"
    tweetsfontcolor = "#3d3d3d"
    tweetslinkscolor = "#0c59cc"
    profile = ""

    def __init__(self, tpinterval=30000, tpwidth=250, tpheight=300, shellbackground="#feb200", shellfontcolor="#262626", tweetsbackground="#ffffff", tweetsfontcolor="#3d3d3d", tweetslinkscolor="#0c59cc", profile="", **kwargs):
        self.tpinterval = tpinterval
        self.tpwidth = tpwidth
        self.tpheight = tpheight
        self.shellbackground = shellbackground
        self.shellfontcolor = shellfontcolor
        self.tweetsbackground = tweetsbackground
        self.tweetsfontcolor = tweetsfontcolor
        self.tweetslinkscolor = tweetslinkscolor
        self.profile = profile

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Twitter Widget Portlet Profile"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('twitterwidgetportlet.pt')

    def getScriptProfile(self):
        """ Returns script for the Twitter Portlet
        """
        scriptProfileTwitter="""new TWTR.Widget({
  version: 2,
  type: 'profile',
  rpp: 4,
  interval: %i,
  width: %i,
  height: %i,
  theme: {
    shell: {
      background: '%s',
      color: '%s'
    },
    tweets: {
      background: '%s',
      color: '%s',
      links: '%s'
    }
  },
  features: {
    scrollbar: false,
    loop: false,
    live: false,
    behavior: 'all'
  }
}).render().setUser('%s').start();
        """%(self.data.tpinterval,self.data.tpwidth,self.data.tpheight,self.data.shellbackground, self.data.shellfontcolor,self.data.tweetsbackground,self.data.tweetsfontcolor,self.data.tweetslinkscolor,self.data.profile)
        return scriptProfileTwitter

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ItwitterWidgetPortlet)

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ItwitterWidgetPortlet)
