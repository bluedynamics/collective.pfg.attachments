from Products.Five import BrowserView


#@view_config('attachment_download', permission='view')
#def attachment_download(model, request):
#    attachment = get_attachment(model, request.params['uid'])
#    blob = attachment.attrs['data']
#    handle = blob.open()
#    response = Response()
#    response.body = handle.read()
#    handle.close()
#    response.headers['Content-Type'] = attachment.attrs['mimetype']
#    filename = 'attachment;filename="%s"' % attachment.attrs['filename']
#    response.headers['Content-Disposition'] = filename
#    return response


class SaveDataAndAttachmentsView(BrowserView):
    pass
