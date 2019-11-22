
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

client = language.LanguageServiceClient()

document = types.Document(
    content=u'Doctors without borders is a clinical organization that operates in other countries.',
    type=enums.Document.Type.PLAIN_TEXT)
category = client.classify_text(document)