import mtranslate


def translate(text, source_language, dest_language):
    return mtranslate.translate(text, dest_language, source_language)

    # r = requests.get("http://translate.google.com/m?hl=%s&sl=%s&q=%s"
    #                  % (dest_language, source_language, urllib.request(text)))
    #
    # if r.status_code != 200:
    #     return _("Error: the translation service failed.")
    # return json.loads(r.content)
