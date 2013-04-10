from Products.CMFCore.permissions import setDefaultRoles


PROJECTNAME = 'collective.pfg.attachments'
ADD_PERMISSIONS = {
    'FormSaveDataAndAttachmentsAdapter': \
        'collective.pfg.attachments: Add FormSaveDataAndAttachmentsAdapter',
}
setDefaultRoles(
    ADD_PERMISSIONS['FormSaveDataAndAttachmentsAdapter'],
    ('Manager', 'Owner', 'Contributor', 'Site Administrator')
)
