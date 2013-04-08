from Products.CMFCore.permissions import setDefaultRoles


PROJECTNAME = 'collective.pfg.attachments'
ADD_PERMISSIONS = {
    'FormSaveAttachmentsAdapter': \
        'collective.pfg.attachments: Add FormSaveAttachmentsAdapter',
}
setDefaultRoles(
    ADD_PERMISSIONS['FormSaveAttachmentsAdapter'],
    ('Manager', 'Owner', 'Contributor', 'Site Administrator')
)
