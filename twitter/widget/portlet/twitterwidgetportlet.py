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
    tptitle = schema.TextLine(title=_(u"Title"),
                                  description=_(u"Title of the portlet"),
                                  required=False)
    tpsubtitle = schema.TextLine(title=_(u"Subtitle"),
                                  description=_(u"Subtitle of the portlet"),
                                  required=False)
    tpsearch = schema.TextLine(title=_(u"Name, profile or hashtag to be searched"),
                                  description=_(u"Name, profile or hashtag to be searched"),
                                  required=False)
    portletSearchType = schema.Tuple(title=_(u"Type of Portlet"),
                    description=_(u"If enabled it will require the field to be searched, "
                                           "if not enabled, it will require only a profile"),
                    required=True,
                    value_type=schema.Choice(
                    values=['Search', 'Profile']))

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

    tptitle = ""
    tpsubtitle = ""
    tpsearch = ""
    portletSearchType = ['Search']
    tpinterval = 30000
    tpwidth = 250
    tpheight = 300
    shellbackground = "#feb200"
    shellfontcolor = "#262626"
    tweetsbackground = "#ffffff"
    tweetsfontcolor = "#3d3d3d"
    tweetslinkscolor = "#0c59cc"
    profile = ""

    def __init__(self, tptitle="", tpsubtitle="",tpsearch="",portletSearchType=('Search',), tpinterval=30000, tpwidth=250, tpheight=300, shellbackground="#feb200", shellfontcolor="#262626", tweetsbackground="#ffffff", tweetsfontcolor="#3d3d3d", tweetslinkscolor="#0c59cc", profile="", **kwargs):
        self.tptitle = tptitle
        self.tpsubtitle = tpsubtitle
        self.tpsearch = tpsearch
        self.portletSearchType = portletSearchType
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
        return "Twitter Widget Portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('twitterwidgetportlet.pt')

    def getScriptSearch(self):
        """ Returns script for the Twitter Portlet
        """
        scriptSearchTwitter="""new TWTR.Widget({
  version: 2,
  type: 'search',
  search: '%s',
  interval: %i,
  title: '%s',
  subject: '%s',
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
    loop: true,
    live: true,
    behavior: 'default'
  }
}).render().start();
        """%(self.data.tpsearch,self.data.tpinterval,self.data.tptitle,self.data.tpsubtitle,self.data.tpwidth,self.data.tpheight,self.data.shellbackground, self.data.shellfontcolor,self.data.tweetsbackground,self.data.tweetsfontcolor,self.data.tweetslinkscolor)
        return scriptSearchTwitter

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

    def getType(self):
        """ Returns true if portlet type is Search, false if is Profile
        """
        portletST=True
        if self.data.portletSearchType=="Search":
            portletST=True
        else:
            portletST=False
        return portletST

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ItwitterWidgetPortlet)

    def create(self, data):
        return Assignment(**data)


# NOTE: If this portlet does not have any configurable parameters, you
# can use the next AddForm implementation instead of the previous.

# class AddForm(base.NullAddForm):
#     """Portlet add form.
#     """
#     def create(self):
#         return Assignment()


# NOTE: If this portlet does not have any configurable parameters, you
# can remove the EditForm class definition and delete the editview
# attribute from the <plone:portlet /> registration in configure.zcml


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ItwitterWidgetPortlet)
