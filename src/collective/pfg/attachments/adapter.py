import uuid
import datetime
from types import StringTypes
from ZODB.blob import Blob
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations
from AccessControl import ClassSecurityInfo
from Products.CMFPlone.utils import safe_hasattr
from Products.Archetypes import atapi
from Products.ATContentTypes.content.base import registerATCT
from Products.PloneFormGen.config import LP_SAVE_TO_CANONICAL
from Products.PloneFormGen.content.saveDataAdapter import FormSaveDataAdapter
from . import config


class Attachment(PersistentDict):

    def __init__(self, filename, mimetype, enc, data):
        self.attrs['filename'] = filename
        self.attrs['mimetype'] = mimetype
        self.attrs['enc'] = enc
        self.attrs['data'] = Blob(data)
        self.attrs['created'] = datetime.datetime.now()


class FormSaveDataAndAttachmentsAdapter(FormSaveDataAdapter):

    schema = FormSaveDataAdapter.schema.copy() + atapi.Schema(())

    meta_type      = 'FormSaveDataAndAttachmentsAdapter'
    portal_type    = 'FormSaveDataAndAttachmentsAdapter'
    archetype_name = 'Save Data And Attachments Adapter'

    immediate_view = 'fg_savedataandattachments_view'
    default_view   = 'fg_savedataandattachments_view'
    suppl_views    = ('fg_savedataandattachments_view',)

    security       = ClassSecurityInfo()

    def onSuccess(self, fields, REQUEST=None, loopstop=False):
        if LP_SAVE_TO_CANONICAL and not loopstop:
            # LinguaPlone functionality:
            # check to see if we're in a translated
            # form folder, but not the canonical version.
            parent = self.aq_parent
            if safe_hasattr(parent, 'isTranslation') and \
               parent.isTranslation() and not parent.isCanonical():
                # look in the canonical version to see if there is
                # a matching (by id) save-data adapter.
                # If so, call its onSuccess method
                cf = parent.getCanonical()
                target = cf.get(self.getId())
                if target is not None \
                  and target.meta_type == 'FormSaveDataAdapter':
                    target.onSuccess(fields, REQUEST, loopstop=True)
                    return

        ANNOTATION_KEY = 'formgen_attachments'
        annotations = IAnnotations(self)
        attachments = annotations.get(ANNOTATION_KEY, None)
        if attachments is None:
            attachments = PersistentDict()
            annotations[ANNOTATION_KEY] = attachments

        from ZPublisher.HTTPRequest import FileUpload

        data = []
        for f in fields:
            showFields = getattr(self, 'showFields', [])
            if showFields and f.id not in showFields:
                continue
            if f.isFileField():
                file = REQUEST.form.get('%s_file' % f.fgField.getName())
                if isinstance(file, FileUpload) and file.filename != '':
                    file.seek(0)
                    fdata = file.read()
                    filename = file.filename
                    mimetype, enc = guess_content_type(filename, fdata, None)
                    attachment = Attachment(filename, mimetype, enc, fdata)
                    attachment_id = str(uuid.uuid4())
                    attachments[attachment_id] = attachment
                    data.append('attachment:%s' % attachment_id)
                else:
                    data.append('NO UPLOAD')
            elif not f.isLabel():
                val = REQUEST.form.get(f.fgField.getName(), '')
                if not type(val) in StringTypes:
                    # Zope has marshalled the field into
                    # something other than a string
                    val = str(val)
                data.append(val)

        if self.ExtraData:
            for f in self.ExtraData:
                if f == 'dt':
                    data.append(str(DateTime()))
                else:
                    data.append(getattr(REQUEST, f, ''))

        self._addDataRow(data)


registerATCT(FormSaveDataAndAttachmentsAdapter, config.PROJECTNAME)
