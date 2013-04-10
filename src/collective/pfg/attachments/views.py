from zope.annotation.interfaces import IAnnotations
from Products.Five import BrowserView
from . import config


class Attachments(BrowserView):

    @property
    def attachments(self):
        annotations = IAnnotations(self.context)
        return annotations.get(config.ANNOTATION_KEY, {})


class DownloadAttachment(Attachments):

    def __call__(self):
        uid = self.request['f']
        attachment = self.attachments.get(uid)
        if not attachment:
            raise IOError('file not found')
        response = self.request.response
        response.setHeader('Content-Type', attachment['mimetype'])
        response.setHeader('Content-Disposition',
                           'attachment; filename=%s' % attachment['filename'])
        blob = attachment['data']
        handle = blob.open()
        body = handle.read()
        handle.close()
        return body


class SaveDataAndAttachmentsView(Attachments):

    @property
    def colnames(self):
        return self.context.getColumnNames();

    @property
    def rows(self):
        attachments = self.attachments
        result = self.context.getSavedFormInput();
        ret = list()
        for res_row in result:
            row = list()
            for res_col in res_row:
                col = dict()
                if res_col.startswith('__fg_attachment__:'):
                    uid = res_col[18:]
                    attachment = attachments.get(uid)
                    if not attachment:
                        col['type'] = 'string'
                        col['value'] = 'Attachment not found'
                        continue
                    col['type'] = 'attachment'
                    col['value'] = attachment['filename']
                    col['mimetype'] = attachment['mimetype']
                    col['url'] = '%s/download_attachment?f=%s' % (
                        self.context.absolute_url(), uid)
                else:
                    col['type'] = 'string'
                    col['value'] = res_col
                row.append(col)
            ret.append(row)
        return ret
